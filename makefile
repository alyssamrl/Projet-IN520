.PHONY: compile run test clean

lex.yy.c: regexp.l
	lex regexp.l

y.tab.c y.tab.h: regexp.y
	yacc -d regexp.y

compile: lex.yy.c y.tab.c
	gcc -o compile lex.yy.c y.tab.c

run: compile
	./compile < test.1
	python3 main.py


test: test-etoile test_determinisation test-egal test-union test-concat test-complet test-toutfaire


test-etoile:
	python3 test_etoile.py

test-determinisation:
	python3 test_determinisation.py

test-egal:
	python3 test_egal.py

test-union:
	python3 test_union.py

test-concat:
	python3 test_concat.py

test-complet:
	python3 test_complet.py

test-toutfaire:
	python3 test_toutfaire.py

clean:
	rm -f lex.yy.c y.tab.c y.tab.h compile main.py
	rm -rf __pycache__