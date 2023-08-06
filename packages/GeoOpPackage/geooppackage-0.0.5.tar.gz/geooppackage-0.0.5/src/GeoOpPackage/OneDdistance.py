import math
 
def distance(*args):
    if len(args)==2:
        x1 = args[0]
        x2 = args[1]
        if(type(x1).__name__ in ['int', 'float'] and type(x2).__name__ in ['int', 'float']):
                if(x1>=0 and x2>=0):
                    return math.fabs(x2 - x1)
                else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"


