
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
    num_0=0
    printf_0("请输入排序的整数个数:\n")
    scanf_0("%d",&num_0)
    arr_0=[None]*100
    printf_0("请输入相应数量的整数:\n")
    i_0=0
    while i_0<num_0:
        scanf_0("%d",&arr_0[i_0])
        i_0=i_0+1
    i_1=0
    while i_1<num_0:
        j_0=0
        while j_0<num_0:
            if arr_0[j_0]>arr_0[i_1]:
                temp_0=arr_0[i_1]
                arr_0[i_1]=arr_0[j_0]
                arr_0[j_0]=temp_0
            j_0=j_0+1
        i_1=i_1+1
    printf_0("排序好的数组为:\n")
    i_1=0
    while i_1<num_0:
        printf_0("%d ",arr_0[i_1])
        i_1=i_1+1
    printf_0("\n")
    return 0

if __name__ == "__main__":
    main_0()
