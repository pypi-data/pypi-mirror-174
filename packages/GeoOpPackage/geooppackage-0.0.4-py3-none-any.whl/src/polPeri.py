#Perimeter of regular polygon

def perimeter(*args):
        if len(args)==2:
                s = args[0]
                n = args[1]
                if(type(s).__name__ in ['int', 'float'] and type(n).__name__ in ['int', 'float']):
                        perimeter = 1
                        perimeter = n * s
                        if(s>=0 and n>=0):
                                return perimeter
                        else:
                                return "Invalid input"
                else:
                        return "Invalid Input" 
        else:
                return "Please enter only 2 arguments"



# print(Perimeter(2,4))