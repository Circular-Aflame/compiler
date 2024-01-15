
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

def gets_0(s):
    s_in = input()
    for i, c in enumerate(s_in):
        s[i] = c

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

def main_0():
    i_0 = None
    n_0=0
    a_0=[None]*999
    *p_0=a_0
    printf_0("输入待检测字符串：")
    gets_0(a_0)
    while a_0[n_0]:
        n_0=n_0+1
    i_0=0
    while *(p_0+i_0)==*(p_0+n_0-1):
        n_0=n_0-1
        i_0=i_0+1
    if n_0-i_0<=2:
        printf_0("该字符串回文yes\n")
    else:
        printf_0("该字符串不回文no\n")
    return 0

if __name__ == "__main__":
    main_0()
