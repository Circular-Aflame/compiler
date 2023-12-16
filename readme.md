# compiler

## 环境配置
安装ply库用于词法和语法分析
```
pip install ply
```

## 词法分析
利用ply库的lex模块实现词法分析。参考ply[http://www.dabeaz.com/ply/ply.html]手册。定义token和保留字等参照了C语言标准文档1999[https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf]