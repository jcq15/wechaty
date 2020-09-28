import datetime
import json
import logging
import random
import math
import itertools
import numpy as np
import re

'''这样记录日志
logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
'''

class Baoshi:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename='/home/wechat/wechatbot/output.log')
        self.logger = logging.getLogger(__name__)
        self.model = r'frog2.0启动！淦！已经\h点\m分了！你今天学习了吗？'
        self.function = '我是青蛙！我有这些功能，都要@我噢！\n'\
                           '1. 发送“功能”查看功能；\n'\
                           '2. 发送“报时”报时；\n'\
                           '3. 发送“24点”，给你四个数算24点。一定能算出来，算不出来说明你是傻逼；\n'\
                           '4. 发送“48点”，给你四个数算48点。一定能算出来，算不出来说明你是大傻逼；\n'\
                           '5. 发送“计算 表达式”进行计算，例如“计算 114000+514”'

    # 获取报时内容
    def __gettext(self):
        response_text = ''
        status = False
        for c in self.model:
            if not status:
                if c == chr(92):
                    status = True
                else:
                    response_text += c
            else:
                status = False
                if c == chr(92):
                    response_text += c
                elif c == 'h':
                    response_text += str(datetime.datetime.now().hour)
                elif c == 'm':
                    response_text += str(datetime.datetime.now().minute)
                elif c == 's':
                    response_text += str(datetime.datetime.now().second)
                else:
                    pass
        return response_text

    def __infix_evaluator(self, infix_expression : str):
        '''这是中缀表达式求值的函数
        :参数 infix_expression:中缀表达式
        '''
        def get_value(operator : str, op1 : int, op2 : int):
            '''这是四则运算函数
            :参数 operator:运算符
            :参数 op1:左边的操作数
            :参数 op2:右边的操作数
            '''
            if operator == '+':
                return op1 + op2
            elif operator == '-':
                return op1 - op2
            elif operator == '*':
                return op1 * op2
            elif operator == '/':
                return op1 / op2
        infix_expression = infix_expression.replace('（', '(').replace('）', ')').replace(' ', '')
        token_list = re.split("([+-/\*\(\)])", infix_expression)
        print(token_list)
        # 运算符优先级字典
        pre_dict = {'*':3,'/':3,'+':2,'-':2,'(':1}
        # 运算符栈
        operator_stack = []
        # 操作数栈
        operand_stack = []
        for token in token_list:
            if not token:
                continue
            # 数字进操作数栈
            if token.isdecimal() or token[1:].isdecimal():
                operand_stack.append(int(token))
            # 左括号进运算符栈
            elif token == '(':
                operator_stack.append(token)
            # 碰到右括号，就要把栈顶的左括号上面的运算符都弹出求值
            elif token == ')':
                top = operator_stack.pop()
                while top != '(':
                    # 每弹出一个运算符，就要弹出两个操作数来求值
                    # 注意弹出操作数的顺序是反着的，先弹出的数是op2
                    op2 = operand_stack.pop()
                    op1 = operand_stack.pop()
                    # 求出的值要压回操作数栈
                    # 这里用到的函数get_value在下面有定义
                    operand_stack.append(get_value(top,op1,op2))
                    # 弹出下一个栈顶运算符
                    top = operator_stack.pop()
            # 碰到运算符，就要把栈顶优先级不低于它的都弹出求值
            elif token in '+-*/':
                while operator_stack and pre_dict[operator_stack[-1]] >= pre_dict[token]:
                    top = operator_stack.pop()
                    op2 = operand_stack.pop()
                    op1 = operand_stack.pop()
                    operand_stack.append(get_value(top,op1,op2))
                # 别忘了最后让当前运算符进栈
                operator_stack.append(token)
        # 表达式遍历完成后，栈里剩下的操作符也都要求值   
        while operator_stack:
            top = operator_stack.pop()
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            operand_stack.append(get_value(top,op1,op2))
        # 最后栈里只剩下一个数字，这个数字就是整个表达式最终的结果
        return operand_stack[0]
     
    def handle(self, data):
        if data['mentionSelf']:
            text = data['text'].replace('@青蛙 ', '').replace('@青蛙\u2005', '')

            if len(text) >= 6 and text[:4] == '修改模板':
                self.model = text[5:]
                return '修改成功！现在的模板是：\n' + self.model

            elif text == '功能':
                return self.function

            elif text == '报时':
                return self.__gettext()

            elif len(text) >= 4 and text[:2] == '计算':
                _, expression = text.split(' ')
                return str(self.__infix_evaluator(text[3:]))

            elif text == 'ping':
                return str(data['age'])

            elif text == '24点':
                num_list = []    
                array_data = np.loadtxt('/home/wechat/wechatbot/24p_1_9.txt')
                len(list(array_data))
                id=np.random.randint(low=0, high=len(list(array_data)))
                choice = list(array_data)[id]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                return '4 numbers:' + res

            elif text == '48点':
                num_list = []    
                array_data = np.loadtxt('/home/wechat/wechatbot/48p_1_13.txt')
                len(list(array_data))
                id=np.random.randint(low=0, high=len(list(array_data)))
                choice = list(array_data)[id]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                return '4 numbers:' + res
