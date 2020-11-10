import ProblemFileHandler as handler
import OJTemplate

# 生成一个题目文件
# 第一种方法：problem_text_file + test_cases_file
text_file1 = '../resources/OJ/demo_problem1_text.txt'
test_cases_file1 = '../resources/OJ/demo_problem1_test_cases.txt'
output_file1 = '../resources/OJ/Problems/Problem1.plm'
handler.generate_problem(problem_text_file=text_file1,
                         test_cases_file=test_cases_file1,
                         output_file=output_file1,
                         overwrite=True)

# 第二种方法：problem_text_file + standard_answer_func + test_inputs
# 注意此时test_cases_file必须为None（默认）

text_file2 = '../resources/OJ/demo_problem2_text.txt'
answer_func = OJTemplate.standard_answer
inputs = OJTemplate.test_inputs
output_file2 = '../resources/OJ/Problems/Problem2.plm'
handler.generate_problem(problem_text_file=text_file2,
                         standard_answer_func=answer_func,
                         test_inputs=inputs,
                         output_file=output_file2,
                         overwrite=True)

# 读取Problem文件（.plm），返回包含'text'和'test_cases'两个key的字典

problem_dict1 = handler.load_problem_file(output_file1)
problem_dict2 = handler.load_problem_file(output_file2)

print(problem_dict1)
print(problem_dict2)