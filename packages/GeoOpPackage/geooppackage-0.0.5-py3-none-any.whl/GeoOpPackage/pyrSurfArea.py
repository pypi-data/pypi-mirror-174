def SqPyrSA(*args):
        if len(args)==2:
                BaseLen = args[0]
                SlantHeight = args[1]
                if(type(BaseLen).__name__ in ['int', 'float'] and type(SlantHeight).__name__ in ['int', 'float']):
                        if(BaseLen>=0 and SlantHeight>=0):
                                return(2*BaseLen*SlantHeight + BaseLen*BaseLen)
                        else:
                                return "Invalid input"
                else:
                        return "Invalid Input" 
        else:
                return "Please enter only 2 arguments"


def TriPyrSA(*args):
        if len(args)==3:
                BaseHeight = args[0]
                BaseLength = args[1]
                SideHeight = args[2]
                if(type(BaseHeight).__name__ in ['int', 'float'] and type(BaseLength).__name__ in ['int', 'float'] and type(SideHeight).__name__ in ['int', 'float']):
                        if(BaseHeight>=0 and BaseLength>=0 and SideHeight>=0):
                                return 0.5*BaseHeight*BaseLength + 1.5*BaseLength*SideHeight
                        else:
                                return "Invalid input"
                else:
                        return "Invalid Input" 
        else:
                return "Please enter only 3 arguments"


def PentPyrSA(*args):
        if len(args)==3:
                BaseHeight = args[0]
                BaseLength = args[1]
                SideHeight = args[2]
                if(type(BaseHeight).__name__ in ['int', 'float'] and type(BaseLength).__name__ in ['int', 'float'] and type(SideHeight).__name__ in ['int', 'float']):
                        if(BaseHeight>=0 and BaseLength>=0 and SideHeight>=0):
                                return 2.5*BaseHeight*BaseLength + 2.5*BaseLength*SideHeight
                        else:
                                return "Invalid input"
                else:
                        return "Invalid Input" 
        else:
                return "Please enter only 3 arguments"

def HexPyrSA(*args):
        if len(args)==3:
                BaseHeight = args[0]
                BaseLength = args[1]
                SideHeight = args[2]
                if(type(BaseHeight).__name__ in ['int', 'float'] and type(BaseLength).__name__ in ['int', 'float'] and type(SideHeight).__name__ in ['int', 'float']):
                        if(BaseHeight>=0 and BaseLength>=0 and SideHeight>=0):
                                return 3*BaseHeight*BaseLength + 3*BaseLength*SideHeight
                        else:
                                return "Invalid input"
                else:
                        return "Invalid Input" 
        else:
                return "Please enter only 3 arguments"


