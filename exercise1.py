def calculateMultiplicationTable(polynom):
    e = len(polynom) - 1 
    maxBinaryValue = pow(2, e)
    for xCount in range(1, maxBinaryValue):
        x = f'{xCount:0{e}b}'
        for yCount in range(1, maxBinaryValue):
            y = f'{yCount:0{e}b}'
            product = multiply(x, y)
            reduced = reduce(f'{int(product, 2):0{e}b}', e, polynom)
         #   print(x + ' * ' + y + ' = ' + reduced)

def multiply(x, y):
    product = [0] * (len(x) + len(y) - 1)
    for indexA, aChar in enumerate(x):
        for indexB, bChar in enumerate(y):
            product[indexA+indexB] += int(aChar, 2) * int(bChar, 2)
    return ''.join(str(p % 2) for p in product)
            
def reduce(term, e, polynom):
    gradTerm = len(term) - term.find('1') if term.find('1') != -1 else 0
    gradPolynom = len(polynom) - polynom.find('1')
    if gradTerm < gradPolynom:
        return term[-e:]
    else:
        shiftedPolynom = f'{int(polynom, 2) << (gradTerm - gradPolynom):0{gradTerm}b}'
        reducedTerm = f'{int(term, 2) ^ int(shiftedPolynom, 2):0{e}b}'
        return reduce(reducedTerm, e, polynom)


def main(var,x,y,z):
    # calculateMultiplicationTable('111')
    calculateMultiplicationTable(var)

    result = multiply(x, y)
    finalResult = multiply(result, z)
    print('(x*y)*z=', finalResult)
    result1 = reduce(finalResult, 2, var)
    print(finalResult, f'modulo {var}: ', result1)

    result = multiply(y, z)
    finalResult = multiply(result, x)
    print('x*(y*z)=', finalResult)
    reduce(finalResult, 2, var)
    result2 = reduce(finalResult, 2, var)
    print(finalResult, f'modulo {var}: ', result2)

    if result1 == result2:
        print('Die erzielten Ergebnisse sind gleich: ', result1, '=', result2)
    else:
        print('Die erzielten Ergebnisse sind nicht gleich: ', result1, '!=', result2)

def test(var,x,y,z):
    # calculateMultiplicationTable('111')
    calculateMultiplicationTable(var)

    result = multiply(x, y)
    finalResult = multiply(result, z)
    result1 = reduce(finalResult, 2, var)

    result = multiply(y, z)
    finalResult = multiply(result, x)
    reduce(finalResult, 2, var)
    result2 = reduce(finalResult, 2, var)

    return result1 == result2



if __name__ == "__main__":
    # main('1101','100','111','010')
    # main('11001','1000','1111','0101')
    # main('110001','11000','11111','00100')
    main('1100001','100000','111111','101011')

    exceptioncase=[]
    workingcase=[]
    notworkingcase=[]

    for i in range(0,20):
        for j in range(0,20):
            for k in range(0,20):
                for l in range(0,20):
                    var = "{0:b}".format(l)
                    x = "{0:b}".format(k)
                    y="{0:b}".format(i)
                    z="{0:b}".format(j)
                    case=[var,x,y,z]
                    try:
                        if test(var,x,y,z):
                            workingcase.append(case)
                        else:
                            notworkingcase.append(case)
                    except:
                        exceptioncase.append(case)
        
    print(f'Working cases for [var, x,y,z]: {workingcase}, \n\n\n not working cases: {notworkingcase}, \n\n\n exceptioncases: {exceptioncase}')
