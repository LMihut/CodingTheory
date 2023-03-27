import math

def getPrimitiveElement(q, irreduciblePolynom):
    bodyElements = []
    for i in range(1, q):
        bodyElements.append(i)

    for alpha in range(2, q):
        alphaElements = generateAlphaElements(alpha, q, irreduciblePolynom)
        sortedAlphaElements = sorted(alphaElements)
        sortedBodyElements = sorted(bodyElements)
        if sortedAlphaElements == sortedBodyElements:
            return alpha

def generateAlphaElements(a, q, irreduciblePolynom):
    wordLength = int(math.log2(q))
    alphaElements = []
    alphaElements.append(f'{1:0{wordLength}b}')
    for i in range(1, q - 1):
        alphaElement = f'{a:0{wordLength}b}'
        tmp = f'{a:0{wordLength}b}'
        for _ in range(1, i):
            tmp = multiplyPolynom(tmp, alphaElement)
            tmp = reduce(tmp, wordLength, irreduciblePolynom)
        alphaElements.append(tmp)
    return list(((int(p, 2)) for p in alphaElements))

def generateGeneratorAndControlPolynom(q, d, p, irreduciblePolynom):
    divider = generateAlphaElements(p, q, irreduciblePolynom)

    generatorDividers = divider[1: d]
    generatorPolynom = [1, generatorDividers[0]]
    for i in range(1, len(generatorDividers)): # multiply each element
        m1 = ''.join(str(p) for p in generatorPolynom)
        m2 = '1' + ''.join(str(p) for p in [generatorDividers[i]])
        generatorPolynom = multiply(m1, m2, q, irreduciblePolynom)
        while True: # pop the zeros
            if generatorPolynom[0] == 0:
                generatorPolynom = generatorPolynom[1:]
            else: 
                break


    controlDividers = [divider[0]] + divider[d:q - 1]
    controlPolynom = [1, controlDividers[0]]
    for i in range(1, len(controlDividers)): # multiply each element
        m1 = ''.join(str(p) for p in controlPolynom)
        m2 = '1' + ''.join(str(p) for p in [controlDividers[i]])
        controlPolynom = multiply(m1, m2, q, irreduciblePolynom)
        while True: # pop the zeros
            if controlPolynom[0] == 0:
                controlPolynom = controlPolynom[1:]
            else: 
                break
    
    return generatorPolynom[::-1], controlPolynom[::-1] # flip from big-to-small to small-to-big

def multiply(x, y, q, irreduceblePolynom):
    wordLength = int(math.log2(q))
    y = y.zfill(len(y) + (len(x) - len(y)))
    product = [f'{0:0{wordLength}b}'] * (len(x) + len(y) - 1)
    for indexA, aChar in enumerate(x):
        aNum = int(aChar)
        for indexB, bChar in enumerate(y):
            bNum = int(bChar)
            prod = multiplyPolynom(f'{aNum:0{wordLength}b}', f'{bNum:0{wordLength}b}')
            reducedProd = reduce(prod, wordLength, irreduceblePolynom)
            currentProdAtIndex = int(product[indexA + indexB], 2)
            product[indexA + indexB] = f'{int(reducedProd, 2) ^ currentProdAtIndex:0{wordLength}b}'
    return list(((int(p, 2) % q) for p in product))

def multiplyPolynom(x, y):
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

def generateMatrix(x, y, polynom):
    matrix = []
    paddedPolynom = polynom + [0] * (x - len(polynom))
    for i in range(y):
        Rfirst = paddedPolynom[0 : len(paddedPolynom) - i]
        Rsecond = paddedPolynom[len(paddedPolynom) - i : ]
        matrix.append(Rsecond + Rfirst)

    return matrix

def generateVanderMondeMatrix(q, d, p, irreduciblePolynom):
    wordLength = int(math.log2(q))
    vanderMondeMatrix = [ [0] * (q - 1) for _ in range((d - 1))]
    for i in range(1, d):
        for j in range(q - 1):
            if i * j == 0: 
                vanderMondeMatrix[i - 1][j] = 1
            else:
                product = f'{p:0{wordLength}b}'
                for _ in range(1, i * j):
                    product = multiplyPolynom(product, f'{p:0{wordLength}b}')
                    product = reduce(product, wordLength, irreduciblePolynom)
                vanderMondeMatrix[i - 1][j] = int(product, 2)

    return vanderMondeMatrix


def main(q,d,irreduciblePolynom):
    primitiveElement = getPrimitiveElement(q, irreduciblePolynom)
    print('Primitive Element: ')
    print(primitiveElement)
    generatorPolynom, controlPolynom = generateGeneratorAndControlPolynom(q, d, primitiveElement, irreduciblePolynom)
    print('Generator Polynom: ')
    print(generatorPolynom)
    print('Control Polynom: ')
    print(controlPolynom)
    generatorMatrix = generateMatrix(q - 1, q - d, generatorPolynom)
    print('Generator Matrix: ')
    print(generatorMatrix)
    controlMatrix = generateMatrix(q - 1, d - 1, controlPolynom[::-1]) # controlPolynom has to be flipped again
    print('Control Matrix: ')
    print(controlMatrix)
    vanderMondeMatrix = generateVanderMondeMatrix(q, d, primitiveElement, irreduciblePolynom)
    print('VanderMonde Matrix: ')
    print(vanderMondeMatrix)

def test(q,d,irreduciblePolynom):
    primitiveElement = getPrimitiveElement(q, irreduciblePolynom)
    generatorPolynom, controlPolynom = generateGeneratorAndControlPolynom(q, d, primitiveElement, irreduciblePolynom)
    generatorMatrix = generateMatrix(q - 1, q - d, generatorPolynom)
    controlMatrix = generateMatrix(q - 1, d - 1, controlPolynom[::-1]) # controlPolynom has to be flipped again
    vanderMondeMatrix = generateVanderMondeMatrix(q, d, primitiveElement, irreduciblePolynom)

if __name__ == "__main__":
    # main(8,3,'1101')
    # main(8,2,'1101')
    # main(8,4,'1101')
    # main(8,9,'1101')
    exceptioncase=[]
    workingcase=[]

    for q in range(0,50):
        for d in range(0,50):
            for i in range(0,50):
                polynom = "{0:b}".format(i)
                case=[q,d,polynom]
                try:
                    test(q,d,polynom)
                    workingcase.append(case)
                except:
                    exceptioncase.append(case)
    
    print(f'Working cases for [q,d,i]: {workingcase}, \n\n\n not working cases: {exceptioncase}')

            

    

