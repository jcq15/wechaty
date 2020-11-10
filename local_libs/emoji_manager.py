import emoji


class EmojiManager:

    def __init__(self):
        self.SELECTOR = '\ufe0f'

    def text2emoji(self, txt):
        print('text to emoji')
        estr = emoji.emojize(txt, use_aliases=True, variant='emoji_type')
        print(len(estr))
        print(estr)

        for ch in estr:
            print(ch, hex(ord(ch)))

    def emoji2text(self, emoji):
        print('emoji to text')


if __name__ == '__main__':
    manager = EmojiManager()
    manager.text2emoji(':thumbsup:')
    print(u'\U0001f44dfe0f')
