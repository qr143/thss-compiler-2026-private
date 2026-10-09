lexer grammar SysYLexer;

CONST    : 'const';
INT      : 'int';
VOID     : 'void';
IF       : 'if';
ELSE     : 'else';
WHILE    : 'while';
BREAK    : 'break';
CONTINUE : 'continue';
RETURN   : 'return';

PLUS  : '+';
MINUS : '-';
MUL   : '*';
DIV   : '/';
MOD   : '%';

ASSIGN : '=';

EQ  : '==';
NEQ : '!=';
LT  : '<';
GT  : '>';
LE  : '<=';
GE  : '>=';

NOT : '!';
AND : '&&';
OR  : '||';

L_PAREN  : '(';
R_PAREN  : ')';
L_BRACE  : '{';
R_BRACE  : '}';
L_BRACKT : '[';
R_BRACKT : ']';

COMMA     : ',';
SEMICOLON : ';';

// TODO: (Part1) finish the implementation of IDENT and INTEGER_CONST
IDENT         : ;
INTEGER_CONST : ;

WS : [ \t\r\n]+ -> skip ;
LINE_COMMENT : '//' .*? '\n' -> skip ;

// TODO: (Part1) finish the implementation of MULTILINE_COMMENT
MULTILINE_COMMENT : ;

// Optional: you can add some fragment rules to help you implement IDENT, INTEGER_CONST, and MULTILINE_COMMENT
