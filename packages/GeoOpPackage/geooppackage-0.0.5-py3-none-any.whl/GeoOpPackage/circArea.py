import math

def circArea(*args):
    if len(args)==1:
        r = args[0]
        if(type(r).__name__ in ['int', 'float']):
                if(r>0):
                    return math.pi* pow(r,2)
                else:
                    return "Invalid input"
        else:
                return "Invalid Input" 
    else:
        return "Please enter only 1 argument"
