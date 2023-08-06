import math
pi = math.pi
sqrt = math.sqrt
 
def coneVol(*args):
    if len(args)==2:
        r = args[0]
        h = args[1]
        if(type(r).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
            if(r>=0 and h>=0):
                return (1 / 3) * pi * r * r * h
            else:
                return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 1 argument"
 
def coneSurf(*args):
    if len(args)==2:
        r = args[0]
        s = args[1]
        if(type(r).__name__ in ['int', 'float'] and type(s).__name__ in ['int', 'float']):
                if(r>=0 and s>=0):
                    return pi * r * s + pi * r * r
                else:
                    return "Invalid input"
        else:
                return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"


def coneLatSurf(*args):
    if len(args)==2:
        r = args[0]
        h = args[1]
        if(type(r).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
                if(r>=0 and h>=0):
                    return pi * r * sqrt((h*h)+(r*r))
                else:
                    return "Invalid input"
        else:
                return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"