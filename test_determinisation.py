from automate2 import*

a=automate("a")
b=automate("b")
u=union(a,b)
s=supression_epsilon_transitions(u)
d=determinisation(s)
print(d)