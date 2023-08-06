def factorial(number):
    fact = 1
    if number < 0:
        print("Factorial for negative numbers don't exist...")
    else:
        for i in range(1,number+1):
            fact = fact*i
            i = i+1
    return fact


def armstrong(number):

    sum = 0

    tempoarary = number
    while tempoarary > 0:
        remainder = tempoarary % 10
        sum += remainder ** 3
        tempoarary //= 10

    if number == sum:
        return True
    else:
        return False


def decimal(binary):
    decimal,i,n = 0,0,0
    while (binary != 0):
        remainder = binary % 10
        decimal = decimal + remainder * 2 ** i
        binary = binary // 10
        i = i+1
    return decimal


def binary(decimal):
    bin = 0
    ctr = 0
    temp = decimal  #copy input decimal
    #find binary value using while loop
    while(temp > 0):
         bin = ((temp%2)*(10**ctr)) + bin
         temp = int(temp/2)
         ctr += 1
    return bin


def peterson(n): 
    num = n 
    sum_val = 0
    while n > 0: 
        digit = int(n % 10) 
        sum_val += factorial(digit) 
        n = int(n / 10) 
    if num==sum_val:
        return True
    else:
        return False

def primeFactors(n):
    if n < 4:
        return n
    arr = []
    while n > 1:
        for i in range(2, int(2+n//2)):
            if i == (1 + n // 2):
                arr.append(n)
                n = n // n
            if n % i == 0:
                arr.append(i)
                n = n // i
                break
    return arr

def perfectSquare(x):
       if(x >= 0):
           #sr = int(math.sqrt(x))
           sr = x**0.5
           return ((sr*sr) == x)
       return False

