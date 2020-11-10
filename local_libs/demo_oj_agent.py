import PyOJAgent

# Problem 1 正确解答
submission1_correct = """
def add(a, b):
    for i in range(10):
        pass

    return a + b

def other_function():
    pass
    # print('nonsense')

def main_function(a, b):
    other_function()
    return add(a, b)
"""

# Problem 1 超时解答
submission1_TLE = """
def main_function(a, b):
    while(True):
        pass
"""

# Problem 1 语法错误
submission1_CE = """
defmain_function(a, b):
    while(True):
        pass
"""

# Problem 1 结果错误
submission1_WA = """
def main_function(a, b):
    for i in range(10):
        pass

    return a - b
"""

# Problem 1 运行时错误
submission1_RE = """
def main_function(a, b):
    return 1 / 0
"""

# Problem 1 未按要求定义main_function
submission1_UNDEF = """
def add(a, b):
    return a + b
"""

submission1_correct_with_class = """

class Foo:
    def __init__(self):
        pass
    
    def add(self, a, b):
        return a + b
    
def main_function(a, b):
    f = Foo()
    return f.add(a, b)

"""

submission2_correct = """
def main_function(a):
    max_element = -1e20
    current = 0

    for i in range(len(a)):
        if a[i] >= max_element:
            current = i
            max_element = a[i]

    return current
"""

submission2_incorrect = """
def main_function(a):
    return 1
"""

if __name__ == '__main__':
    agent = PyOJAgent.PyOJAgent(memory_limit=102400, time_limit=1)
    agent.load_problem_file('../resources/OJ/Problems/Problem1.plm')
    print(agent.describe_problem())

    print('\n\n==============测试：正解（包含类定义）================')
    agent.test_submission(submission1_correct_with_class)
    print(agent.report_submission_result())

    print('\n\n==============测试：正解（不包含类定义）================')
    agent.test_submission(submission1_correct)
    print(agent.report_submission_result())

    print('\n\n==============测试：编译错误================')
    agent.test_submission(submission1_CE)
    print(agent.report_submission_result())

    print('\n\n==============测试：错误答案================')
    agent.test_submission(submission1_WA)
    print(agent.report_submission_result())

    print('\n\n==============测试：超时================')
    agent.test_submission(submission1_TLE)
    print(agent.report_submission_result())

    print('\n\n==============测试：运行时错误================')
    agent.test_submission(submission1_RE)
    print(agent.report_submission_result())

    print('\n\n==============测试：未按要求定义函数================')
    agent.test_submission(submission1_UNDEF)
    print(agent.report_submission_result())

    # ======================== 第二题 ============================

    agent.load_problem_file('../resources/OJ/Problems/Problem2.plm')
    print(agent.describe_problem())

    print('\n\n==============测试：第2题正解================')
    agent.test_submission(submission2_correct)
    print(agent.report_submission_result())

    print('\n\n==============测试：第2题错解================')
    agent.test_submission(submission2_incorrect)
    print(agent.report_submission_result())
