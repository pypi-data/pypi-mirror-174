import math
pi = math.pi
sqrt = math.sqrt
 
def cylVol(*args): 
    if len(args)==2:
        r = args[0]
        h = args[1]
        if(type(r).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
            if(r>0 and h>0):
                return pi * r * r * h
            else:
                return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"


def cylSurf(*args):
    if len(args)==2:
        r = args[0]
        h = args[1]

        if(type(r).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
            if(r>0 and h>0):
                return 2*pi*r*(h + r)
            else:
                return "Invalid input"
        else:
                return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"


def cylLatSurf(*args):
    if len(args)==2:
        r = args[0]
        h = args[1]
        if(type(r).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
            if(r>0 and h>0):
                return 2 * pi * r * h
            else:
                return "Invalid input"
        else:
                return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"

    #print(cylVol(9,5))