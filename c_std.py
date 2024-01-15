# C 中的gets函数
gets_py='''
def gets_0(s):
    s_in = input()
    for i, c in enumerate(s_in):
        s[i] = c
'''

# C 中的printf函数
printf_py = '''
def printf_0(format_str, *args):
    new_args = []
    for arg in args:
        if type(arg) == list:
            s = ''
            for c in arg:
                if c == None:
                    break
                s += c
            arg = s
        new_args.append(arg) 
    print(format_str % tuple(new_args), end='')
'''

# C 中的printf函数
scanf_py = '''
def scanf_0(format_str, *args):
    values = input(format_str).split()  # 从用户输入获取值
    formatted_args = []

    for expected_type, value in zip(args, values):
        if expected_type == int:
            formatted_args.append(int(value))
        elif expected_type == float:
            formatted_args.append(float(value))
        elif expected_type == str:
            formatted_args.append(value)
        else:
            raise ValueError("Unsupported data type")

    return tuple(formatted_args)
'''


# C 中的strlen函数，这里通过None判断数组末尾
strlen_py = '''
def strlen_0(s):
    if isinstance(s, str):
        return len(s)
    else:
        _len = 0
        for i in s:
            if i is None:
                break
            _len += 1
        return _len
'''

# C 中的fgets函数
fgets_py = '''
def fgets_0(s, size, stream):
    s_in = input()
    for i, c in enumerate(s_in):
        if i == size - 1:
            break
        s[i] = c
    s[size - 1] = '\\0'
'''

# C 中的sizeof函数
sizeof_py = '''
def sizeof_0(s):
    if isinstance(s, str):
        return len(s) + 1
    else:
        _len = 0
        for i in s:
            if i is None:
                break
            _len += 1
        return _len + 1
'''


c_stds = [strlen_py, gets_py, printf_py, scanf_py, fgets_py, sizeof_py]