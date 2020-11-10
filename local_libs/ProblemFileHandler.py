import json


class ProblemFileHandler:

    def __init__(self):
        pass

    @staticmethod
    def generate_problem(problem_text_file=None, test_cases_file=None, output_file=None,
                         standard_answer_func=None, test_inputs=None,
                         overwrite=False):
        # Two ways of generating a problem:
        # 1. problem_text_file + test_cases_file
        # 2. problem_text_file + standard_answer_func + test_inputs (test_cases_file must be None)

        with open(problem_text_file, encoding='utf-8') as f:
            text = f.read()

        if test_cases_file:
            with open(test_cases_file) as f:
                test_cases = json.load(f)
        else:
            test_cases = ProblemFileHandler.generate_test_points(standard_answer_func, test_inputs)

        problem_dict = {'text': text, 'test_cases': test_cases}

        if overwrite:
            mode = 'w'
        else:
            mode = 'x'

        with open(output_file, mode, encoding='utf-8') as f:
            json.dump(problem_dict, f, ensure_ascii=False)

    @staticmethod
    def load_problem_file(problem_file):
        problem_dict = {}

        try:
            f = open(problem_file, encoding='utf-8')
            problem_dict = json.load(f)
        except Exception as e:
            print(repr(e))

        return problem_dict

    @staticmethod
    def generate_test_points(standard_answer_func, test_inputs):
        test_cases = [(test_point, standard_answer_func(*test_point)) for test_point in test_inputs]

        return test_cases

    @staticmethod
    def generate_from_memory(txt, tp, output_file):

        oj_dict = {'txt': txt, 'tp': tp}

        with open(output_file, 'x', encoding='utf-8') as f:
            json.dump(oj_dict, f, ensure_ascii=False)

