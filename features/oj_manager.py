from features.feature_manager import ReflectiveManager
from local_libs.PyOJAgent import PyOJAgent


class OJManager(ReflectiveManager):
    def __init__(self):
        super().__init__(private_enabled=False)
        self.user_config = {}

    def reflective_handle(self, data) -> list:
        args, code = self.preprocess(data)
        recipient = ReflectiveManager.get_source(data)

        if not args or len(args) < 2:
            return self.make_null_response()
        else:
            if not self.user_config.get(recipient):
                self.user_config[recipient] = [PyOJAgent(), False]  # second is in-progress flag
            else:
                pass

            oj_agent = self.user_config[recipient][0]

            if args[0].lower() == 'oj':
                try:
                    problem_id = int(args[1])
                except ValueError as e:
                    # print(repr(e))
                    msg = '请输入合法的题号！'
                else:
                    oj_filename = self.abs_path + 'resources/OJ/Problems/Problem' + str(problem_id) + '.plm'
                    success = oj_agent.load_problem_file(oj_filename)

                    if not success:
                        msg = '田了！题库里没这题！'
                    else:
                        msg = oj_agent.describe_problem()

                return ReflectiveManager.reply_text(msg, data, with_mention=True)
            elif args[0].lower() == '提交oj':
                if self.user_config[recipient][1]:
                    msg = '上一个OJ还没测试完呢，先等会儿！急什么！'
                else:
                    self.user_config[recipient][1] = True
                    oj_agent.test_submission(code)
                    self.user_config[recipient][1] = False

                    msg = oj_agent.report_submission_result()

                return ReflectiveManager.reply_text(msg, data, with_mention=True)
            else:
                return self.make_null_response()



