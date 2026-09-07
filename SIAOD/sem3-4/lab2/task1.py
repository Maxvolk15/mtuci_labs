from decimal import Decimal
from fractions import Fraction

def Float(n1):
    i = float(n1)
    return (i*0.97+(i*0.97*0.2))/3

def Decimal_task(n2):
    j = Decimal(n2)
    return (j*Decimal('0.97')+(j*Decimal('0.97')*Decimal('0.2')))/Decimal('3')

def Fraction_task(n3):
    k = Fraction(n3)
    return (k*Fraction('0.97')+(k*Fraction('0.97')*Fraction('0.2')))/Fraction('3')

prices = [19.99, 5.49, 3.50, 12.30, 49.64, 31.01, 7.99]
for h in prices:
    print(f"{h}: Float: {Float(h)}, Decimal: {Decimal_task(h)}, Fraction: {Fraction_task(h)}")