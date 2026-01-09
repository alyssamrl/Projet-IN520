from automate2 import *

a = automate("a")
complet = completion(a)
print(complet)

x = automate("a")
y = automate("b")
u = union(x, y)
s = supression_epsilon_transitions(u)  # IMPORTANT
c = completion(s)
print(c)

w = automate("a")
z = automate("b")
ct = concatenation(w, z)
su = supression_epsilon_transitions(ct)
cp = completion(su)
print(cp)
