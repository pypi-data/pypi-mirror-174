def factorial(number):
    fact = 1
    if number < 0:
        print("Factorial for negative numbers don't exist...")
    else:
        for i in range(1,number+1):
            fact = fact*i
            i = i+1
    return fact



