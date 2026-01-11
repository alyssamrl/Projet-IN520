

%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

int yylex(void);
void yyerror(const char *s);

char* RESULT=NULL;

char* mkstr(const char* s) {
    char* r= malloc(strlen(s)+1);
    strcpy(r,s);
    return r;
}


char* mk2(const char* a, const char* b, const char* c) {
    char* r=malloc(strlen(a) + strlen(b)+strlen(c)+1);
    strcpy(r,a);
    strcat(r,b);
    strcat(r,c);
    return r;
}
%}

%union {
    char*s;
}

%token SYM_A SYM_B SYM_C EPSILON
%token PLUS CONCAT STAR
%token PAR_O PAR_F

%type <s> expr term factor base
%start input
%%

input:
    expr
    | input expr
    ;

expr : 
     expr PLUS term {
        $$=mk2("union(",mk2($1,",",$3), ")");
        printf("%s\n", $$);
     }
    | term { 
        $$=$1;
        printf("%s\n", $$);
    }
    ;


term : 
     term CONCAT factor {
        $$=mk2("concatenation(",mk2($1,",",$3), ")");
     }
    | factor { $$=$1; }
    ;


factor : 
     base STAR {
        $$=mk2("etoile(",$1,")");
     }
    | base { $$=$1; }
    ;

base :
     SYM_A {$$=mkstr("automate('a')");}
    | SYM_B {$$=mkstr("automate('b')");}
    | SYM_C {$$=mkstr("automate('c')");}
    | EPSILON {$$=mkstr("automate('E')");}
    | PAR_O expr PAR_F {$$=$2;}
    ;

%%

int main(void) {
    return yyparse();
}

void yyerror(const char *s) {
    printf("il y a une erreur\n");
}