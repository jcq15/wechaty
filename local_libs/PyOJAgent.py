from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import Guards
from RestrictedPython import safe_globals
from RestrictedPython import utility_builtins
from RestrictedPython.PrintCollector import PrintCollector
from multiprocessing import Process
from multiprocessing import Manager
import local_libs.ProblemFileHandler as Handler
import time


class PyOJAgent:
    def __init__(self, memory_limit=1048576, time_limit=5):
        self.name = 'default_agent'
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.submission_result = []
        self.problem_dict = {}
        self.compile_error_flag = False
        self.compile_error_info = ''
        self.problem_file_handler = Handler.ProblemFileHandler()

    def load_problem_file(self, problem_file):
        self.problem_dict = self.problem_file_handler.load_problem_file(problem_file)

        if self.problem_dict:
            return True
        else:
            return False

    def test_submission(self, submission_code_str):
        self.submission_result = []
        self.compile_error_flag = False

        if not self.problem_dict:
            return
        else:
            pass

        try:
            compile_restricted(submission_code_str, '<inline>', 'exec')
        except Exception as e:
            self.compile_error_flag = True
            self.compile_error_info = repr(e)

            return

        for test_case in self.problem_dict['test_cases']:
            print('testing test case:', test_case, sep='\n')
            suffix = '\noutput = main_function' + str(tuple(test_case[0]))

            try:
                manager = Manager()
                py_code = submission_code_str + suffix
                ret_dict = manager.dict()
                p = Process(target=target_function, args=(py_code, ret_dict))
                p.start()
                time.sleep(self.time_limit)
                p.terminate()
                p.join()

                if not ret_dict:
                    self.submission_result.append('服务器资源不足！')
                    return
                else:
                    print('submission result: ', ret_dict['output'])

                    if ret_dict['RE_flag']:
                        self.submission_result.append('Runtime Error! ' + ret_dict['RE_info'])
                    elif ret_dict['TLE_flag']:
                        self.submission_result.append('Time Limit Exceeded! ')
                    elif ret_dict['output'] == test_case[1]:
                        self.submission_result.append('Accepted! ')
                    else:
                        self.submission_result.append('Wrong Answer! ')  # add error types here maybe
            except Exception as e:
                print(repr(e))

    def report_submission_result(self):
        if self.compile_error_flag:
            return "Compile Error!\n" + self.compile_error_info
        elif not self.problem_dict:
            return '未加载题目！'
        elif not self.submission_result:
            return 'No Report Available!'
        else:
            ret = ''
            n = len(self.submission_result)
            ret += '{0}组数据已测试，结果如下：\n'.format(n)

            for i in range(n):
                ret += '测试点{0}/{1}：'.format(i + 1, n)
                ret += self.submission_result[i]
                ret += '\n'

            return ret

    def describe_problem(self):

        if not self.problem_dict:
            return '未加载题目！'
        else:
            ret = '题目描述：\n'
            ret += self.problem_dict['text']
            ret += '\n========\n'
            ret += '附加信息：\n'
            ret += '本次测试时间限制：{0} s，内存限制：{1} KB\n'.format(self.time_limit, self.memory_limit)

            return ret

    def reset(self):
        self.submission_result = []
        self.problem_dict = {}


# this function has to be defined outside the PyOJAgent class for multiprocessing to pickle
def target_function(py_code, ret_dict):
    policy_globals = generate_restricted_environment_policy()
    policy_globals['output'] = None

    ret_dict['RE_flag'] = False
    ret_dict['RE_info'] = ''
    ret_dict['TLE_flag'] = True
    ret_dict['output'] = None

    try:
        byte_code = compile_restricted(py_code, '<inline>', 'exec')
        exec(byte_code, policy_globals)
        ret_dict['TLE_flag'] = False
        ret_dict['output'] = policy_globals['output']
    except Exception as e:
        print(repr(e))
        ret_dict['RE_flag'] = True      # if RE, TLE flag would also be True
        ret_dict['RE_info'] = repr(e)
    finally:
        pass
        # print('finally')


def generate_restricted_environment_policy():
    policy_globals = {**safe_globals, **utility_builtins}
    policy_globals['__builtins__']['__metaclass__'] = type
    policy_globals['__builtins__']['__name__'] = type

    policy_globals['_getattr_'] = Guards.safer_getattr
    policy_globals['_write_'] = Guards.full_write_guard
    policy_globals['_getiter_'] = Eval.default_guarded_getiter
    policy_globals['_getitem_'] = Eval.default_guarded_getitem
    policy_globals['_print_'] = PrintCollector
    policy_globals['_iter_unpack_sequence_'] = Guards.guarded_iter_unpack_sequence

    return policy_globals