from local_libs.puppet_contact import PuppetContact
import baoshi
agent = baoshi.Baoshi()


def data_parser(txt):
    data = {
        'mentionSelf': True,
        'contact': PuppetContact(idx=9),
        'text': txt
    }

    return data


data1 = {'mentionSelf': True,
         'contact': PuppetContact(idx=9),
         'text': '今日运势 双子座'}

data2 = {'mentionSelf': True,
         'contact': PuppetContact(idx=9),
         'text': '成语接龙'}

if __name__ == '__main__':
    ret = agent.handle(data1)
    print(ret)
    ret = agent.handle(data2)
    print(ret)

    while True:
        txt = input('please talk to frog: ')
        data = data_parser(txt)
        print(agent.handle(data))
