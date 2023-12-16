# compiler
朱旭 覃诗睿

## 环境配置
安装ply库用于词法和语法分析
```
pip install ply
```

## 词法分析
利用ply库的lex模块实现词法分析。参考[ply](http://www.dabeaz.com/ply/ply.html)手册。定义token和保留字等参照了[C语言标准文档ISO/IEC 9899:TC3](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf)。
### 创新点
1. 可以忽略两种类型的注释
    ```
    // 注释一
    /* 注释二 */
    ```
2. 加入了宏定义符号识别
    识别#,方便后续预编译处理。

## 小组分工
朱旭：词法分析
覃诗睿：测试程序