%option noyywrap
%{
#include <stdio.h>
#include "regexp.tab.h"

/*
#define SYM_A 1
#define SYM_B 2
#define SYM_C 3
#define EPSILON 4
#define PLUS 5
#define CONCAT 6
#define STAR 7
#define PAR_O 8
#define PAR_F 9
*/
%}

%%
"a" {return SYM_A; }
"b" { return SYM_B; }
"c" { return SYM_C; }
"E" { return EPSILON; }

"+" { return PLUS; }
"\." { return CONCAT; }
"*" { return STAR; }

"(" { return PAR_O; }
")" { return PAR_F; }

[ \t\n]+  ;
%%
