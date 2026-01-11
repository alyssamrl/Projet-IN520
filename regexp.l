%option noyywrap
%{
#include <stdio.h>
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



/*
. { 
    printf("Caractère invalide : %s\n", yytext); 
    /* return yytext[0]; */
} */


/*
int main(void) {
    int t;
    while ((t = yylex()) != 0) {
        printf("Token reconnu : %d\n", t);
    }
    return 0;
}
*/

/*
int yywrap(void) {
    return 1;
} 
*/

