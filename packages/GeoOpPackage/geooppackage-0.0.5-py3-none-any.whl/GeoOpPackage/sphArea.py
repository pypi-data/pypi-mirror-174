import math
pi = math.pi
 
def sphVol(*args):
    if len(args)==1:
        r = args[0]
        if(type(r).__name__ in ['int', 'float']):
            if(r>=0):
                return (1.3333)*pi * r * r * r 
            else:
                return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 1 argument"

 
def sphSurf(*args):
    if len(args)==1:
        r = args[0]
        if(type(r).__name__ in ['int', 'float']):
            if(r>=0):
                return 4*pi*r*r 
            else:
                return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 1 argument"
