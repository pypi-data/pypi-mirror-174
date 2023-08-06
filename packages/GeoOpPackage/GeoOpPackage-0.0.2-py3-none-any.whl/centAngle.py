import math

def centAngle(*args):
    if len(args)==2:
        diameter = args[0]
        arcLen = args[1]

        if(type(diameter).__name__ in ['int', 'float'] and type(arcLen).__name__ in ['int', 'float']):
                if(diameter>=0 and arcLen>=0):
                    centAngle = (arcLen*360.0)/ (math.pi*diameter) 
                    return centAngle
                else:
                    return "Invalid input"
        else:
                return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"