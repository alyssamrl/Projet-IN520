from automate2 import *
a=automate("a")
b=automate("b")
u=union(a,b)
e=etoile(u)
print(e)