

import subprocess
from automate2 import automate, concatenation, union, etoile, tout_faire,egal


lignes=[]
with open("test.1") as f:
    for ligne in f:
            L=ligne.strip()
            if L!="":
                 lignes.append(L)

codes=[]
for regex in lignes:
    out=subprocess.check_output(
        ["./regex_parser"],
        input=regex + "\n",
        text=True
    )
    codes.append(out.strip())

a1=tout_faire(eval(codes[0]))
a2=tout_faire(eval(codes[1]))

if egal(a1,a2):
    print("EGAL")
else:
    print("NON EGAL")