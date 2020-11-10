from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import Guards
from RestrictedPython import safe_globals
from RestrictedPython import utility_builtins

from multiprocessing import Process, Manager
import time
import os       # os is unavailable in user code scope even we imported os
import math   # math is available in user code scope even we did not import math
import random


def shit(mask, target, total_length):
    if total_length < 2:
        return 'shit: too short!'
    else:
        pos = random.randint(1, total_length)
        return mask * pos + target + mask * (total_length - pos)


def generate_safe_policy():
    policy_globals = {**safe_globals, **utility_builtins}
    policy_globals['__builtins__']['__metaclass__'] = type
    policy_globals['__builtins__']['__name__'] = type
    policy_globals['_getattr_'] = Guards.safer_getattr
    policy_globals['_write_'] = Guards.full_write_guard
    policy_globals['_getiter_'] = Eval.default_guarded_getiter
    policy_globals['_getitem_'] = Eval.default_guarded_getitem
    policy_globals['_iter_unpack_sequence_'] = Guards.guarded_iter_unpack_sequence
    policy_globals['shoot'] = shit

    return policy_globals


def safe_calculate_without_time_limit(input_str, return_list, tle_str):
    policy_globals = generate_safe_policy()
    ret = tle_str

    try:
        bytecode = compile_restricted(input_str, '<calc_exp>', 'eval')
        result = eval(bytecode, policy_globals)
    except Exception as e:
        ret = repr(e)
    else:
        ret = str(result)
    finally:
        return_list.append(ret)
        #print(return_list)
        return ret


def safe_calculate(input_str, time_limit=1):
    with Manager() as manager:

        tle_str = 'Calculate Time out! {0}s'.format(time_limit)
        return_list = manager.list()
        p = Process(target=safe_calculate_without_time_limit, args=(input_str, return_list, tle_str))
        p.start()
        time.sleep(time_limit)
        p.terminate()
        p.join()
        # print(return_list)

        if return_list:
            return return_list[0]
        else:
            return 'Calculate Time out! {0}s'.format(time_limit)
