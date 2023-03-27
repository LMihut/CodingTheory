import exercise1

def calculateMultiplicativeInverse(polynom):
    e = len(polynom) - 1 
    maxBinaryValue = pow(2, e)
    for xCount in range(1, maxBinaryValue):
        x = f'{xCount:0{e}b}'
        s = eea(x, polynom)
        quotient, inverse = divide(s, polynom)
        remainderOfCheck = check(x, s, polynom)

        print('The inverse of ' + x + ' mod ' + polynom + ' is ' + inverse + '. The check should return 1: ' + remainderOfCheck)

def divide(a, b):
    degA = len(a) - a.find('1') if a.find('1') != -1 else 0
    degB = len(b) - b.find('1')
    quotient = ''

    degDiff = degA - degB

    # pad b to same length and add same amount to quotient
    for i in range(degDiff):
        b = b + '0'
        quotient += '0'
    
    # add 1 to quotient depending on the degDiff
    if degDiff > 0:
        quotient = '1' + quotient
    else:
        quotient = quotient + '1'

    remainder = f'{int(a, 2) ^ int(b, 2):0b}'
    remainderDeg = len(remainder) - remainder.find('1') if remainder.find('1') != -1 else 0

    if remainderDeg >= degB:
        newQuotient, newRemainder = divide(remainder, b)

        quotient = f'{int(quotient, 2) ^ int(newQuotient, 2):0b}'
        remainder = newRemainder

    return quotient, remainder
            
def eea(a, b):
    oldR = a
    r = b
    oldS = '1'
    s = '0'
    oldT = '0'
    t = '1'

    while int(r, 2) != 0:
        quotient, remainder = divide(oldR, r)

        oldR = r
        r = remainder
        
        tempS = oldS
        oldS = s
        s = f'{int(tempS, 2) ^ int(exercise1.multiply(quotient, s), 2):0b}'

        tempT = oldT
        oldT = t
        t = f'{int(tempT, 2) ^ int(exercise1.multiply(quotient, t), 2):0b}'
    
    return oldS

def check(x, s, polynom):
    e = len(polynom) - 1
    prod = exercise1.multiply(x, s)
    reduced = exercise1.reduce(f'{int(prod, 2):0{e}b}', e, polynom)
    quotient, remainder = divide(reduced, polynom)
    return remainder


def test(polynom):
    e = len(polynom) - 1 
    maxBinaryValue = pow(2, e)
    for xCount in range(1, maxBinaryValue):
        x = f'{xCount:0{e}b}'
        s = eea(x, polynom)
        quotient, inverse = divide(s, polynom)
        remainderOfCheck = check(x, s, polynom)

        return remainderOfCheck
        # print('The inverse of ' + x + ' mod ' + polynom + ' is ' + inverse + '. The check should return 1: ' + remainderOfCheck)

if __name__ == "__main__":
    calculateMultiplicativeInverse('111')
    # calculateMultiplicativeInverse('1101')
    # calculateMultiplicativeInverse('11001')
    # calculateMultiplicativeInverse('110001')
    # calculateMultiplicativeInverse('1100001')
    # calculateMultiplicativeInverse('1100001')
    # calculateMultiplicativeInverse('10001111')

    exceptioncase=[]
    workingcase=[]

    for i in range(0,5000):
        t=test("{0:b}".format(i))
        case=["{0:b}".format(i),t]
        if t == None:
            exceptioncase.append(case)
        else:
            if int(t) == 1:  
                workingcase.append(case)
            else:
                exceptioncase.append(case)
            

    print(f'Working cases for [i]: {workingcase}, \n\n\n not working cases: {exceptioncase}')

