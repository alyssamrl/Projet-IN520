from automate2 import *

a=concatenation(automate("a"), automate("c"))
b=concatenation(automate("b"), automate("c"))

a1=tout_faire(a)
b1=tout_faire(b)

print(egal(a1, b1))