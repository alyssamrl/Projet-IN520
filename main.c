
#include <stdio.h>

extern char* RESULT;
int yyparse(void);

int main() {
    yyparse();
    if (RESULT !=NULL) {
        printf("%s\n", RESULT);
    }
    return 0;
}