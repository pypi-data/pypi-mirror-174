import math

def circum(*args):
        if len(args)==1:
            r = args[0]
            if(type(r).__name__ in ['int', 'float']):
                if(r>=0):
                    return math.pi*2*r
                else:
                    return "Invalid input"
            else:
                return "Invalid Input"
        else:
            return "Type Error. Invalid number of arguments"


        # len(getargspec(circum).args) == 1
        



# def func(a, b):
#     pass
#     print(len(getargspec(func).args))
    
    # else:
    #     print("Invalid input")
    #     sys.exit(1)

# def circum(r,s,t,u,v):
#     r=math.pi
#     return len(sys.argv)