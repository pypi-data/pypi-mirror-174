import math

def arcLen(*args):
    if len(args)==2:
        diameter = args[0]
        angle = args[1]
        if(type(diameter).__name__ in ['int', 'float'] and type(angle).__name__ in ['int', 'float']):
                if(angle <= 360 and angle>=0 and diameter>=0):
                    arc = (math.pi*diameter) * (angle/360.0)
                    return arc
                else:
                    return "Invalid input"
        else:
                return "Invalid Input" 
    else:
        return "Please enter only 1 argument"
         
# Driver Code
# diameter = 25.0
# angle = 75.0
# arc_len = arcLen(diameter, angle)
# print(arc_len)
