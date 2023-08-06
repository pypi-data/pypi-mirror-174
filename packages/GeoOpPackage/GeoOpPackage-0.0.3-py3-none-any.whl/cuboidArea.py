import math
pi = math.pi
sqrt = math.sqrt
 
def cuboidVol(*args):
    if len(args)==3:
        l = args[0]
        b = args[1]
        h = args[2]
        if(type(l).__name__ in ['int', 'float'] and type(b).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
                if(l>=0 and b>=0 and h>=0):
                    return l*b*h
                else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 3 arguments"

        
 
def cuboidSurf(*args):
    if len(args)==3:
        l = args[0]
        b = args[1]
        h = args[2]
        if(type(l).__name__ in ['int', 'float'] and type(b).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
                if(l>0 and b>0 and h>0):
                    return 2*(l*b + b*h + l*h)
                else:
                    return "Invalid input"
        else:
            return "Invalid Input"
    else:
        return "Please enter only 3 arguments" 


def cuboidLatSurf(*args):
    if len(args)==3:
        l = args[0]
        b = args[1]
        h = args[2]
        if(type(l).__name__ in ['int', 'float'] and type(b).__name__ in ['int', 'float'] and type(h).__name__ in ['int', 'float']):
                if(l>0 and b>0 and h>0):
                    return 2*h*(l+b)
                else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    
    else:
        return "Please enter only 3 arguments"