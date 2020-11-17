import json


class ResponseMessage:

    message_types = ['null', 'text', 'image']

    def __init__(self, message_type='null', content='empty', recipients=None, mentions=None):
        self.message_type = message_type
        self.content = content
        self.recipients = recipients
        self.mentions = mentions    # only available for text

    def is_null(self):
        return self.message_type == 'null'

    def to_dict(self):
        result = {'type': self.message_type}

        if not self.is_null():
            result['content'] = self.content
            result['recipients'] = self.recipients if self.recipients else []

            if self.message_type == 'text':
                result['mentions'] = self.mentions if self.mentions else []
            else:
                pass
        else:
            pass

        return result

    @staticmethod
    def list_to_json(responses):
        results = [response.to_dict() for response in responses]

        return json.dumps(results)

    @staticmethod
    def is_null_list(responses):
        for response in responses:
            if not response.is_null():
                return False
            else:
                continue

        return True

    @staticmethod
    def make_null_list():
        return [ResponseMessage()]

