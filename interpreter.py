#Mohammad Mahmud CISC 3160 Final Project

import re, sys

# dict for associating variables to their values
vars = {}

# returns the variable name on the LHS of the assignment
def getIdentifier(x):
	id = re.findall(r"^[a-zA-Z][\w]*", x)
	if id is None: sys.exit("syntax error")
	return id

# returns the expression on RHS of the assignment
def getExpression(x):
	x = x.split("=")[1].strip()
	if x[-1] != ';': sys.exit("syntax error")

	if x.find("(") != -1:
		l, r = x.find("("), x.find(")")
		value = evaluateExpression(x[l+1:r])

	return x[:-1]

# evaluates expression to get value
def evaluateExpression(exp):
    l, r = exp.find("("), exp.find(")") + 1
    if l == -1: return simplify(exp)
    if r == 0: sys.exit("syntax error")

    exp = exp.replace(exp[l:r], str(apply(exp[l+1:r-1])))
    return evaluateExpression(exp)

def fact(x):
    if x[0] == '0' and len(x) > 1: 
        sys.exit("syntax error")
    if x[0] == '-': 
        if x[1:] in vars: return vars[x[1:]]
        num_neg = x.rfind("-") + 1
        x = x[num_neg:]
        return int(x) * -1 if num_neg % 2 == 1 else int(x)
    return vars[x] if x in vars else int(x)
    
# perform operation on 2 terms
def apply(x, y, op):
    if x == "": return y
    if y == "": return x
    
    if op == "+":
        return fact(x) + fact(y)
    if op == "-": 
        return fact(x) - fact(y)
    if op == "*": 
        return fact(x) * fact(y)
    
    
# simplify terms 
def simplify(x):
    for i in range(2):
        #reg = r"-?[0-9]*\*-?[0-9]*" if i == 0 else r"-?[0-9]*[\+-]-?[0-9]*"
        reg = r"\(?-?(?:\d+|[a-zA-Z]\w*)\*-?(?:\d+|[a-zA-Z]\w*)\)?" if i == 0 else r"\(?-?(?:\d+|[a-zA-Z]\w*)[+-]-?(?:\d+|[a-zA-Z]\w*)\)?"
        exp = re.findall(reg, x)
        paren = 1
        
        if any(isinstance(e, tuple) for e in exp):
            reg = r"-?[0-9]*\*-?[0-9]*" if i == 0 else r"-?[0-9]*[\+-]-?[0-9]*"
            exp = re.findall(reg, x)
            paren = 0
            
        for e in exp: 
            old = e
            j = e.find("*" if i == 0 else "+")
            if j == -1: j = e.find("-")
            if j == 0: j = e[1:].find("-") + 1
            if j == 0: return x
            
            a, b, op = e[1:j], e[j+1:-1], e[j]
            if e[0] != "(": a, b = e[:j], e[j+1:]
            e = e.replace(e, str(apply(a, b, op)))
            x = x.replace(old, e) 
            return simplify(x)
    
    if exp == []: return fact(x)
    else: return simplify(x)    


# evaluate each line of input file, 
# store identitifiers and their values in dict
# return variable value
def evaluateLine(line):
	id = getIdentifier(line)[0]
	exp = getExpression(line)
	value = simplify(exp)
	vars[id] = int(value)
	return id + " = " + str(value)


with open(f"tests/{sys.argv[1]}", "r") as input:
	lines = input.read().splitlines()
	for line in lines:
		print(evaluateLine(line), end="\n")

