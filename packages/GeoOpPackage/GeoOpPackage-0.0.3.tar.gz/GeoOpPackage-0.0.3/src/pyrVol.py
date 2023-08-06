def triPyrVol(*args):
    if len(args)==3:
        BaseLen = args[0]
        BaseHeight = args[1]
        PyramidHeight = args[2]
        if(type(BaseLen).__name__ in ['int', 'float'] and type(BaseHeight).__name__ in ['int', 'float'] and type(PyramidHeight).__name__ in ['int', 'float']):
            if(BaseLen>0 and BaseHeight>0 and PyramidHeight>0):
                    return (0.1666) * BaseLen * BaseHeight * PyramidHeight
            else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 3 arguments"

 
def sqPyrVol(*args):
    if len(args)==2:
        BaseLen = args[0]
        PyramidHeight = args[1]
        if(type(BaseLen).__name__ in ['int', 'float']  and type(PyramidHeight).__name__ in ['int', 'float']):
            if(BaseLen>=0 and PyramidHeight>=0):
                    return (0.33) * BaseLen * BaseLen * PyramidHeight
            else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 2 arguments"


def pentPyrVol(*args):
    if len(args)==3:
        BaseLen = args[0]
        BaseHeight = args[1]
        PyramidHeight = args[2]
        if(type(BaseLen).__name__ in ['int', 'float']  and type(BaseHeight).__name__ in ['int', 'float'] and type(PyramidHeight).__name__ in ['int', 'float']):
            if(BaseLen>=0 and BaseHeight>=0 and PyramidHeight>=0):
                    return (0.83) * BaseLen * BaseHeight * PyramidHeight
            else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 3 arguments"

def HexPyrVol(*args):
    if len(args)==3:
        BaseLen = args[0]
        BaseHeight = args[1]
        PyramidHeight = args[2]
        if(type(BaseLen).__name__ in ['int', 'float']  and type(BaseHeight).__name__ in ['int', 'float'] and type(PyramidHeight).__name__ in ['int', 'float']):
            if(BaseLen>=0 and BaseHeight>=0 and PyramidHeight>-0):
                    return BaseLen * BaseHeight * PyramidHeight
            else:
                    return "Invalid input"
        else:
            return "Invalid Input" 
    else:
        return "Please enter only 3 arguments"
