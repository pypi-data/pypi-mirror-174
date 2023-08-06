def sumInterior(*args):
    if len(args)==1:
        n = args[0]
        if(type(n).__name__ in ['int', 'float']):
            if(n>0):
                return ((n - 2) * 180)
            else:
                return "Invalid input"
        else:
            return "Invalid Input"   
    else:
        return "Pleasse enter only 1 argument"  
 
# # Driver code
# n = 5
# print(sumInterior(5))