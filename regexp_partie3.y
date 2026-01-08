%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    int yylex(void);
    void yyerror(const char *s);

%}

%token SYM_A SYM_B SYM_C EPSILON
%token PLUS CONCAT STAR
%token PAR_O PAR_F

%start input 

%%
input :
    expr 
    ;

expr : 
     expr PLUS term 
    | term
    ;


term : 
     term CONCAT factor 
    | factor
    ;


factor : 
     base STAR 
    | base
    ;

base :
     SYM_A 
    | SYM_B 
    | SYM_C 
    | EPSILON 
    | PAR_O expr PAR_F
    ;

%%

int main(void) {
    return yyparse();
}

void yyerror(const char *s) {
    printf("il y a une erreur syntaxique\n");
}