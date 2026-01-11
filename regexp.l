%option noyywrap
%{
#include "regexp.tab.h"
%}

%%
"a" {return SYM_A; }
"b" { return SYM_B; }
"c" { return SYM_C; }
"E" { return EPSILON; }

"+" { return PLUS; }
"." { return CONCAT; }
"*" { return STAR; }

"(" { return PAR_O; }
")" { return PAR_F; }

[ \t\n]+  ;

. { return yytext[0]; }
<<EOF>> { return 0; }
%%



