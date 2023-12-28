# 语法树基类
class Node:
    def __init__(self, type):
        self.type = str(type)

# 语法树 非终结符内部结点类
# type 符号类型
# children 子结点列表
class NonterminalNode(Node):
    def __init__(self, type, children):
        Node.__init__(self, type)
        self.children = children
        for i in range(len(self.children)):
            if not isinstance(self.children[i], Node):
                self.children[i] = TerminalNode(str(self.children[i]), str(self.children[i]))

    def __str__(self):
        return ' '.join(map(str, self.children))

# 语法树 终结符外部结点类
# type 符号类型
# value 值
class TerminalNode(Node):
    def __init__(self, type, value):
        Node.__init__(self, type)
        self.value = str(value)
    def __str__(self):
        return self.value
    
# 打印语法树
def printAST(node):
    if isinstance(node,TerminalNode):
        return {node.type:node.value}
    elif isinstance(node,NonterminalNode):
        ret=[]
        for kid in node.children:
            ret.append(printAST(kid))
        return {node.type:ret}


import re
import ply.yacc as yacc
from lexical import tokens, identifier,lexer

reserved_list = ['true', 'false']

# 开始符号
def p_translation_unit(p):
    ''' translation_unit : external_declaration
                         | translation_unit external_declaration '''
    p[0] = NonterminalNode('translation_unit', p[1:])

# 全局声明
def p_external_declaration(p):
    ''' external_declaration : function_definition
                             | declaration
                             | macro '''
    p[0] = NonterminalNode('external_declaration', p[1:])

# 宏
def p_macro(p):
    ''' macro : MACRO IDENTIFIER IDENTIFIER constant_expression
              | MACRO IDENTIFIER '<' headfile '>'
              | MACRO IDENTIFIER '"' headfile '"' '''
    if len(p) == 5 and not p[3] in reserved_list:
        p[3] = TerminalNode('MACRO_CONSTANT', p[3])
    p[0] = NonterminalNode('macro', p[1:])

# 头文件
def p_headfile(p):
    ''' headfile : IDENTIFIER '.' IDENTIFIER
                 | IDENTIFIER '''
    p[0] = NonterminalNode('headfile', p[1:])

# 声明（定义）
def p_declaration(p):
    ''' declaration : declaration_specifiers ';'
                    | declaration_specifiers init_declarator_list ';' '''
    p[0] = NonterminalNode('declaration', p[1:])

# 初始化声明列表
def p_init_declarator_list(p):
    ''' init_declarator_list : init_declarator
                             | init_declarator_list ',' init_declarator '''
    p[0] = NonterminalNode('init_declarator_list', p[1:])

# 声明
def p_init_declarator(p):
    ''' init_declarator : declarator
                        | declarator '=' initializer '''
    p[0] = NonterminalNode('init_declarator', p[1:])

# 声明修饰符
def p_declaration_specifiers(p):
    ''' declaration_specifiers 	: storage_class_specifier
                                | storage_class_specifier declaration_specifiers
                                | type_specifier
                                | type_specifier declaration_specifiers
                                | type_qualifier
                                | type_qualifier declaration_specifiers
                                | function_specifier
                                | function_specifier declaration_specifiers '''
    p[0] = NonterminalNode('declaration_specifiers', p[1:])

# 储存修饰符
def p_storage_class_specifier(p):
    ''' storage_class_specifier : TYPEDEF
                                | EXTERN
                                | STATIC
                                | AUTO
                                | REGISTER '''
    p[0] = NonterminalNode('storage_class_specifier', p[1:])

# 函数修饰符
def p_function_specifier(p):
    ''' function_specifier : INLINE '''
    p[0] = NonterminalNode('function_specifier', p[1:])

# 类型修饰符
def p_type_specifier(p):
    ''' type_specifier : VOID
                       | CHAR
                       | SHORT
                       | INT
                       | LONG
                       | FLOAT
                       | DOUBLE
                       | SIGNED
                       | UNSIGNED
                       | BOOL
                       | struct_or_union_specifier
                       | enum_specifier '''
    p[0] = NonterminalNode('type_specifier', p[1:])

# 类型限定符
def p_type_qualifier(p):
    ''' type_qualifier : CONST
                       | RESTRICT
                       | VOLATILE '''
    p[0] = NonterminalNode('type_qualifier', p[1:])

# 枚举类型
def p_enum_specifier(p):
    ''' enum_specifier : ENUM '{' enumerator_list '}'
                        | ENUM IDENTIFIER '{' enumerator_list '}'
                        | ENUM '{' enumerator_list ',' '}'
                        | ENUM IDENTIFIER '{' enumerator_list ',' '}'
                        | ENUM IDENTIFIER '''
    if not p[2] == '{' and not p[2] in reserved_list:
        p[2] = TerminalNode('IDENTIFIER', p[2])
    p[0] = NonterminalNode('enum_specifier', p[1:])

# 枚举类型  枚举项列表
def p_enumerator_list(p):
    ''' enumerator_list : enumerator
                        | enumerator_list ',' enumerator '''
    p[0] = NonterminalNode('enumerator_list', p[1:])

# 枚举类型  枚举项
def p_enumerator(p):
    ''' enumerator : IDENTIFIER
                   | IDENTIFIER '=' constant_expression '''
    if not p[1] in reserved_list:
        p[1] = TerminalNode('IDENTIFIER', p[1])
    p[0] = NonterminalNode('enumerator', p[1:])

# 结构体，联合类型定义
def p_struct_or_union_specifier(p):
    ''' struct_or_union_specifier : struct_or_union IDENTIFIER '{' struct_declaration_list '}'
                                  | struct_or_union '{' struct_declaration_list '}'
                                  | struct_or_union IDENTIFIER '''
    if not p[2] == '{' and not p[2] in reserved_list:
        p[2] = TerminalNode('IDENTIFIER', p[2])
    p[0] = NonterminalNode('struct_or_union_specifier', p[1:])

# struct和union关键字
def p_struct_or_union(p):
    ''' struct_or_union : STRUCT
                        | UNION '''
    p[0] = NonterminalNode('struct_or_union', p[1:])

# 结构体或联合类型中的成员变量
def p_struct_declaration_list(p):
    ''' struct_declaration_list : struct_declaration
                                | struct_declaration_list struct_declaration '''
    p[0] = NonterminalNode('struct_declaration_list', p[1:])

# 结构体或联合的单个成员变量
def p_struct_declaration(p):
    ''' struct_declaration : specifier_qualifier_list struct_declarator_list ';' '''
    p[0] = NonterminalNode('struct_declaration', p[1:])

# 类型标识符和类型限定符列表
def p_specifier_qualifier_list(p):
    ''' specifier_qualifier_list : type_specifier specifier_qualifier_list
                                 | type_specifier
                                 | type_qualifier specifier_qualifier_list
                                 | type_qualifier  '''
    p[0] = NonterminalNode('specifier_qualifier_list', p[1:])

# 某个类型的多个标识符
def p_struct_declarator_list(p):
    ''' struct_declarator_list : struct_declarator
                               | struct_declarator_list ',' struct_declarator '''
    p[0] = NonterminalNode('struct_declarator_list', p[1:])

# 单个成员变量
def p_struct_declarator(p):
    ''' struct_declarator : declarator
                          | ':' constant_expression
                          | declarator ':' constant_expression '''
    p[0] = NonterminalNode('struct_declarator', p[1:])

# 单个成员变量
def p_declarator(p):
    ''' declarator : pointer direct_declarator
                   | direct_declarator '''
    p[0] = NonterminalNode('declarator', p[1:])

# 指针类型
def p_pointer(p):
    ''' pointer : '*'
                | '*' type_qualifier_list
                | '*' pointer
                | '*' type_qualifier_list pointer '''
    p[0] = NonterminalNode('pointer', p[1:])

# 类型限定符列表
def p_type_qualifier_list(p):
    ''' type_qualifier_list : type_qualifier
                            | type_qualifier_list type_qualifier '''
    p[0] = NonterminalNode('type_qualifier_list', p[1:])

# 直接声明
def p_direct_declarator(p):
    ''' direct_declarator : IDENTIFIER
                        | '(' declarator ')'
                        | direct_declarator '[' type_qualifier_list assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list ']'
                        | direct_declarator '[' assignment_expression ']'
                        | direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list '*' ']'
                        | direct_declarator '[' '*' ']'
                        | direct_declarator '[' ']'
                        | direct_declarator '(' parameter_type_list ')'
                        | direct_declarator '(' identifier_list ')'
                        | direct_declarator '(' ')' '''
    if len(p) == 2 and not p[1] in reserved_list:
        p[1] = TerminalNode('IDENTIFIER', p[1])
    p[0] = NonterminalNode('direct_declarator', p[1:])

# 标识符 列表
def p_identifier_list(p):
    ''' identifier_list : IDENTIFIER
                        | identifier_list ',' IDENTIFIER '''
    if len(p) == 2 and not p[1] in reserved_list:
        p[1] = TerminalNode('IDENTIFIER', p[1])
    elif len(p) == 4 and not p[3] in reserved_list:
        p[3] = TerminalNode('IDENTIFIER', p[3])
    p[0] = NonterminalNode('identifier_list', p[1:])

# 赋值表达式
def p_assignment_expression(p):
    ''' assignment_expression : conditional_expression
                              | unary_expression assignment_operator assignment_expression '''
    p[0] = NonterminalNode('assignment_expression', p[1:])

# 赋值运算符
def p_assignment_operator(p):
    ''' assignment_operator : '='
                            | MUL_ASSIGN
                            | DIV_ASSIGN
                            | MOD_ASSIGN
                            | ADD_ASSIGN
                            | SUB_ASSIGN
                            | LEFT_ASSIGN
                            | RIGHT_ASSIGN
                            | AND_ASSIGN
                            | XOR_ASSIGN
                            | OR_ASSIGN '''
    p[0] = NonterminalNode('assignment_operator', p[1:])

# 常量表达式
def p_constant_expression(p):
    ''' constant_expression : conditional_expression '''
    p[0] = NonterminalNode('constant_expression', p[1:])

# 条件表达式
def p_conditional_expression(p):
    ''' conditional_expression : logical_or_expression
                               | logical_or_expression '?' expression ':' conditional_expression '''
    p[0] = NonterminalNode('conditional_expression', p[1:])

# ||表达式
def p_logical_or_expression(p):
    ''' logical_or_expression : logical_and_expression
                              | logical_or_expression OR_OP logical_and_expression '''
    p[0] = NonterminalNode('logical_or_expression', p[1:])

# &&表达式
def p_logical_and_expression(p):
    ''' logical_and_expression : inclusive_or_expression
                               | logical_and_expression AND_OP inclusive_or_expression '''
    p[0] = NonterminalNode('logical_and_expression', p[1:])

# |表达式
def p_inclusive_or_expression(p):
    ''' inclusive_or_expression : exclusive_or_expression
                                | inclusive_or_expression '|' exclusive_or_expression '''
    p[0] = NonterminalNode('inclusive_or_expression', p[1:])

# ^表达式
def p_exclusive_or_expression(p):
    ''' exclusive_or_expression : and_expression
                                | exclusive_or_expression '^' and_expression '''
    p[0] = NonterminalNode('exclusive_or_expression', p[1:])

# &表达式
def p_and_expression(p):
    ''' and_expression : equality_expression
                       | and_expression '&' equality_expression '''
    p[0] = NonterminalNode('and_expression', p[1:])

# == !=表达式
def p_equality_expression(p):
    ''' equality_expression : relational_expression
                            | equality_expression EQ_OP relational_expression
                            | equality_expression NE_OP relational_expression '''
    p[0] = NonterminalNode('equality_expression', p[1:])

# < > <= >=表达式
def p_relational_expression(p):
    ''' relational_expression : shift_expression
                              | relational_expression '<' shift_expression
                              | relational_expression '>' shift_expression
                              | relational_expression LE_OP shift_expression
                              | relational_expression GE_OP shift_expression '''
    p[0] = NonterminalNode('relational_expression', p[1:])

# << >>表达式
def p_shift_expression(p):
    ''' shift_expression : additive_expression
                         | shift_expression LEFT_OP additive_expression
                         | shift_expression RIGHT_OP additive_expression '''
    p[0] = NonterminalNode('shift_expression', p[1:])

# +表达式
def p_additive_expression(p):
    ''' additive_expression : multiplicative_expression
                            | additive_expression '+' multiplicative_expression
                            | additive_expression '-' multiplicative_expression '''
    p[0] = NonterminalNode('additive_expression', p[1:])

# * / %表达式
def p_multiplicative_expression(p):
    ''' multiplicative_expression : cast_expression
                                  | multiplicative_expression '*' cast_expression
                                  | multiplicative_expression '/' cast_expression
                                  | multiplicative_expression '%' cast_expression '''
    p[0] = NonterminalNode('multiplicative_expression', p[1:])

# 类型转化表达式
def p_cast_expression(p):
    ''' cast_expression : unary_expression
                        | '(' type_name ')' cast_expression '''
    p[0] = NonterminalNode('cast_expression', p[1:])

# 一元表达式
def p_unary_expression(p):
    ''' unary_expression : postfix_expression
                         | INC_OP unary_expression
                         | DEC_OP unary_expression
                         | unary_operator cast_expression
                         | SIZEOF unary_expression
                         | SIZEOF '(' type_name ')' '''
    p[0] = NonterminalNode('unary_expression', p[1:])

# 一元运算符
def p_unary_operator(p):
    ''' unary_operator : '&'
                       | '*'
                       | '+'
                       | '-'
                       | '~'
                       | '!' '''
    p[0] = NonterminalNode('unary_operator', p[1:])

# 后缀表达式
def p_postfix_expression(p):
    ''' postfix_expression : primary_expression
                           | postfix_expression '[' expression ']'
                           | postfix_expression '(' ')'
                           | postfix_expression '(' argument_expression_list ')'
                           | postfix_expression '.' IDENTIFIER
                           | postfix_expression PTR_OP IDENTIFIER
                           | postfix_expression INC_OP
                           | postfix_expression DEC_OP
                           | '(' type_name ')' '{' initializer_list '}'
                           | '(' type_name ')' '{' initializer_list ',' '}' '''
    if len(p) == 4 and not p[2] == '(' and not p[3] in reserved_list:
        p[3] = TerminalNode('IDENTIFIER', p[3])
    p[0] = NonterminalNode('postfix_expression', p[1:])

# 主要表达式
def p_primary_expression(p):
    ''' primary_expression : IDENTIFIER
                           | CONSTANT
                           | STRING_LITERAL
                           | '(' expression ')' '''
    if re.match(r'(([_a-zA-Z])([0-9]|([_a-zA-Z]))*)', p[1]) and not p[1] in reserved_list:
        p[1] = TerminalNode('IDENTIFIER', str(p[1]))
    p[0] = NonterminalNode('primary_expression', p[1:])

# 表达式
def p_expression(p):
    ''' expression : assignment_expression
                   | expression ',' assignment_expression '''
    p[0] = NonterminalNode('expression', p[1:])

# 类型名
def p_type_name(p):
    ''' type_name : specifier_qualifier_list
                  | specifier_qualifier_list abstract_declarator '''
    p[0] = NonterminalNode('type_name', p[1:])

# 抽象声明
def p_abstract_declarator(p):
    ''' abstract_declarator : pointer
                            | direct_abstract_declarator
                            | pointer direct_abstract_declarator '''
    p[0] = NonterminalNode('abstract_declarator', p[1:])

# 直接抽象声明
def p_direct_abstract_declarator(p):
    ''' direct_abstract_declarator : '(' abstract_declarator ')'
                                   | '[' ']'
                                   | '[' assignment_expression ']'
                                   | direct_abstract_declarator '[' ']'
                                   | direct_abstract_declarator '[' assignment_expression ']'
                                   | '[' '*' ']'
                                   | direct_abstract_declarator '[' '*' ']'
                                   | '(' ')'
                                   | '(' parameter_type_list ')'
                                   | direct_abstract_declarator '(' ')'
                                   | direct_abstract_declarator '(' parameter_type_list ')' '''
    p[0] = NonterminalNode('direct_abstract_declarator', p[1:])

# 函数参数 列表
# 推导 -> 普通参数列表|变参列表
def p_parameter_type_list(p):
    ''' parameter_type_list : parameter_list
                            | parameter_list ',' ELLIPSIS '''
    p[0] = NonterminalNode('parameter_type_list', p[1:])

# 函数参数 列表
def p_parameter_list(p):
    ''' parameter_list : parameter_declaration
                       | parameter_list ',' parameter_declaration '''
    p[0] = NonterminalNode('parameter_list', p[1:])

# 函数单个参数声明
def p_parameter_declaration(p):
    ''' parameter_declaration : declaration_specifiers declarator
                              | declaration_specifiers abstract_declarator
                              | declaration_specifiers '''
    p[0] = NonterminalNode('parameter_declaration', p[1:])

# 实参表达式 列表
def p_argument_expression_list(p):
    ''' argument_expression_list : assignment_expression
                                 | argument_expression_list ',' assignment_expression '''
    p[0] = NonterminalNode('argument_expression_list', p[1:])

# 初始化 列表
def p_initializer_list(p):
    ''' initializer_list : initializer
                         | designation initializer
                         | initializer_list ',' initializer
                         | initializer_list ',' designation initializer '''
    p[0] = NonterminalNode('initializer_list', p[1:])

# 初始化 项
def p_initializer(p):
    ''' initializer : assignment_expression
                    | '{' initializer_list '}'
                    | '{' initializer_list ',' '}' '''
    p[0] = NonterminalNode('initializer', p[1:])

def p_designation(p):
    ''' designation : designator_list '=' '''
    p[0] = NonterminalNode('designation', p[1:])

# 指示符 列表
def p_designator_list(p):
    ''' designator_list : designator
                        | designator_list designator '''
    p[0] = NonterminalNode('designator_list', p[1:])

# 指示符
# 例如 -> [XX]  .XX
def p_designator(p):
    ''' designator : '[' constant_expression ']'
                   | '.' IDENTIFIER '''
    if len(p) == 3 and not p[2] in reserved_list:
        p[2] = TerminalNode('IDENTIFIER', p[2])
    p[0] = NonterminalNode('designator', p[1:])

# 函数定义
def p_function_definition(p):
    ''' function_definition : declaration_specifiers declarator declaration_list compound_statement
                            | declaration_specifiers declarator compound_statement '''
    p[0] = NonterminalNode('function_definition', p[1:])

# 声明 列表
def p_declaration_list(p):
    ''' declaration_list : declaration
                         | declaration_list declaration '''
    p[0] = NonterminalNode('declaration_list', p[1:])

# 复合语句（代码块）
def p_compound_statement(p):
    ''' compound_statement : '{' '}'
                           | '{' block_item_list '}' '''
    p[0] = NonterminalNode('compound_statement', p[1:])

# 代码块元素 列表
def p_block_item_list(p):
    ''' block_item_list : block_item
                        | block_item_list block_item '''
    p[0] = NonterminalNode('block_item_list', p[1:])

# 代码块元素
def p_block_item(p):
    ''' block_item : declaration
                   | statement '''
    p[0] = NonterminalNode('block_item', p[1:])

# 语句
def p_statement(p):
    ''' statement : labeled_statement
                  | compound_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement '''
    p[0] = NonterminalNode('statement', p[1:])

# 标记语句
def p_labeled_statement(p):
    ''' labeled_statement : IDENTIFIER ':' statement
                          | CASE constant_expression ':' statement
                          | DEFAULT ':' statement '''
    if len(p) == 4 and not p[1] == 'default' and not p[1] in reserved_list:
        p[1] = TerminalNode('IDENTIFIER', p[1])
    p[0] = NonterminalNode('labeled_statement', p[1:])

# 表达式语句
def p_expression_statement(p):
    ''' expression_statement : ';'
                             | expression ';' '''
    p[0] = NonterminalNode('expression_statement', p[1:])

# 选择语句
def p_selection_statement(p):
    ''' selection_statement : IF '(' expression ')' statement
                            | IF '(' expression ')' statement ELSE statement
                            | SWITCH '(' expression ')' statement '''
    p[0] = NonterminalNode('selection_statement', p[1:])

# 循环语句
def p_iteration_statement(p):
    ''' iteration_statement : WHILE '(' expression ')' statement
                            | DO statement WHILE '(' expression ')' ';'
                            | FOR '(' expression_statement expression_statement ')' statement
                            | FOR '(' expression_statement expression_statement expression ')' statement
                            | FOR '(' declaration expression_statement ')' statement
                            | FOR '(' declaration expression_statement expression ')' statement '''
    p[0] = NonterminalNode('iteration_statement', p[1:])

# 跳转语句
def p_jump_statement(p):
    ''' jump_statement : GOTO IDENTIFIER ';'
                       | CONTINUE ';'
                       | BREAK ';'
                       | RETURN ';'
                       | RETURN expression ';' '''
    if len(p) == 4 and p[1] == 'goto' and not p[2] in reserved_list:
        p[2] = TerminalNode('IDENTIFIER', p[2])
    p[0] = NonterminalNode('jump_statement', p[1:])

# 错误处理
def p_error(p):
    print('[Error]: type - %s, value - %s, lineno - %d, lexpos - %d' % (p.type, p.value, p.lineno, p.lexpos))


# 构建分析器
parser = yacc.yacc()

import json
# 测试程序
if __name__ == '__main__':
    while True:
        try:
            s = input('input file path : ')
            with open(s, 'r') as file:
                result = parser.parse(file.read(),lexer=lexer)
                # 输出为json文件
                with open("AST.json", "w", encoding='utf-8') as f:
                    json.dump(printAST(result), f, indent=2, sort_keys=True, ensure_ascii=False)
        except EOFError:
            break