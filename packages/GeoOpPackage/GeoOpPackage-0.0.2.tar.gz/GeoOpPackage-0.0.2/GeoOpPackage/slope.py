import sys

def slope(*args):
    if len(args)==4:
        x1 = args[0]
        x2 = args[1]
        y1 = args[2]
        y2 = args[3]
        if(type(x1).__name__ in ['int', 'float']  and type(x2).__name__ in ['int', 'float'] and type(y1).__name__ in ['int', 'float'] and type(y2).__name__ in ['int', 'float']):
            if(x1>=0 and x2>=0 and y1>=0 and y2>=0):
                    if(x2 - x1 != 0):
                        return (float)(y2-y1)/(x2-x1)
                    return sys.maxint
            else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 3 arguments"
