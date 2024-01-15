
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

def printf_0(format, *args):
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
    print(format % tuple(new_args), end='')

'list' object has no attribute 'lstrip'
if __name__ == "__main__":
    main_0()
