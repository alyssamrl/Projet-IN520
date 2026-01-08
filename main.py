from automate import *
import os

with open("test.1", "r") as f:
    expr1=f.readline().strip()
    expr2=f.readline().strip()


code1=os.popen(f'echo "{expr1}" | ./regex_parser').read().strip()
code2=os.popen(f'echo "{expr2}" | ./regex_parser').read().strip()

print("CODE 1 =", code1)
print("CODE2 =", code2)

A1=eval(code1)
A2=eval(code2)

if A1==A2:
    print("EGAL")
else:
    print("NON EGAL")