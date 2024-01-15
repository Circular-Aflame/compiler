import os
import re
import black

def format_python_code(input_code):
    '''
    利用black格式化输出的python代码
    返回格式:(bool-是否成功, string-成功返回格式化代码，失败返回错误信息)
    '''
    try:
        formatted_code = black.format_str(input_code, mode=black.FileMode())
        return formatted_code
    except Exception as e:
        return str(e)

def indent(item, rank=-1):
    INDENT_STRING = '    '
    if type(item) == str:
        # 对于只声明不定义的变量需要补上=None
        if '(' not in item and ' ' not in item and '=' not in item and item != '' and item != 'break' \
                and item != 'continue' and item != 'pass' and item != 'else:' and item != 'if' and item != 'return':
            item += ' = None'
        return INDENT_STRING * rank + item
    if type(item) == list:
        lines = []
        for i in item:
            lines.append(indent(i, rank + 1))
        return '\n'.join(lines)

def preprocess(filename):
    """ 
    预处理
    返回格式:(bool-是否成功, string-成功返回预处理过的代码，失败返回错误信息)
    """
    # 文件夹路径，用于寻找include文件路径
    folder = os.path.dirname(filename)
    # 读取文件
    try:
        file = open(filename, 'r', encoding='utf-8')
        lines = file.read().split('\n')
        file.close()
    except FileNotFoundError:
        return False, '打开文件"%s"失败' % filename
    # 宏识别
    macro_define_list = []
    macro_include_list = []
    index = 0
    while index < len(lines):
        line = lines[index]
        line = line.strip(' \t\r\n')
        # 无效行处理
        if len(line) <= 0:
            lines.pop(index)
            continue
        if line[0] == '#':
            words = line[1:].strip(' ').split(' ', 2)
            try:
                # define 识别
                if words[0] == 'define':
                    macro_define_list.append((words[1], words[2]))
                # include 识别
                elif words[0] == 'include':
                    if words[1][0] == '"' and words[1][-1] == '"':
                        macro_include_list.append(os.path.join(folder, words[1][1:-1]))
                    elif words[1][0] == '<' and words[1][-1] == '>':
                        pass
                    else:
                        raise KeyError
                else:
                    raise KeyError
            except KeyError:
                return False, '无效的宏"%s"，来自"%s"' % (line, filename)
            lines.pop(index)
            continue
        index += 1
    # define 处理
    s = '\n'.join(lines)
    for m in macro_define_list:
        s = re.sub(m[0], m[1], s)
    # include 处理
    i = ''
    for m in macro_include_list:
        inc = preprocess(m)
        if inc[0]:
            i = i + inc[1]
        else:
            return inc
    s = i + s + '\n'
    return True, s