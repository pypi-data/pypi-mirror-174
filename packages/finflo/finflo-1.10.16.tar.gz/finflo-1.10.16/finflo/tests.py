# from django.test import TestC


def divide(x, y):
    try:
        # Floor Division : Gives only Fractional
        # Part as Answer
        print("goes her")
        result = x + y
        return result
    except ZeroDivisionError:
        print("Sorry ! You are dividing by zero ")
    finally:
        return "anand"
   
# Look at parameters and note the working of Program
s = divide(3, 2)
print(s)