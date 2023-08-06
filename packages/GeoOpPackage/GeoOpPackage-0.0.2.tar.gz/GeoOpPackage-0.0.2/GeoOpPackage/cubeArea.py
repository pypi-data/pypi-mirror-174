import math
pi = math.pi
 
def cubeVol(*args):
    if len(args)==1:
        s = args[0]
        if(type(s).__name__ in ['int', 'float']):
                if(s>=0):
                    return s*s*s
                else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 1 argument"

 
def cubeSurf(*args):
    if len(args)==1:
        s = args[0]
        if(type(s).__name__ in ['int', 'float']):
                if(s>=0):
                    return 6*s*s
                else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 1 argument"
