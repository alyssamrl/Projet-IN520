%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    int yylex(void);
    void yyerror(const char *s);

    char buffer[10000]="";
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
     expr PLUS term {
       strcat(buffer,"union\n");
     }
    | term
    ;


term : 
     term CONCAT factor {
       strcat(buffer,"concat\n");
     }
    | factor
    ;


factor : 
     base STAR {
       strcat(buffer,"star\n");
     }
    | base
    ;

base :
     SYM_A {strcat(buffer,"a\n"); }
    | SYM_B {strcat(buffer,"b\n"); }
    | SYM_C {strcat(buffer,"c\n"); }
    | EPSILON {strcat(buffer,"E\n");}
    | PAR_O expr PAR_F
    ;

%%

int main(void) {
    yyparse();
    printf("%s", buffer);
    return 0;
}

void yyerror(const char *s) {
   /* erreur ignoree */
}