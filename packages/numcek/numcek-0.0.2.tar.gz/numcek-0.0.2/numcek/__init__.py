from math import remainder


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
        print(number,"is an Armstrong number")
    else:
        print(number,"is not an Armstrong number")


