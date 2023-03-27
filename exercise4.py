import exercise3

def generateControlMatrixFromM(m):
    controlMatrix = [''] * m
    amountOfVectors = pow(2, m) - 1

    for i in range(1, amountOfVectors + 1):
        vector = f'{i:0{m}b}'
        for j in range(len(vector)):
            controlMatrix[j] = controlMatrix[j] + vector[j]

    return controlMatrix


# P is all vectors that are not an einheitsvector
def getPOutOfControlMatrix(matrix):
    pMatrix = []
    transformedMatrix = exercise3.transformMatrix(matrix)

    for i in range(len(transformedMatrix)):
        if transformedMatrix[i].count('1') != 1: # einheitsvector
            pMatrix.append(transformedMatrix[i])

    return pMatrix


def generateGeneratorMatrix(matrix):
    pMatrix = getPOutOfControlMatrix(matrix)
    generatorMatrix = [''] *  len(pMatrix)

    # add the einheitsmatrix
    for i in range(len(generatorMatrix)):
        for j in range(len(generatorMatrix)):
            char = '1' if i == j else '0'
            generatorMatrix[i] = generatorMatrix[i] + char

    # add the P part of the controlMatrix
    for i in range(len(pMatrix)):
        generatorMatrix[i] = generatorMatrix[i] + pMatrix[i]
    
    return generatorMatrix


def generateControlMatrix(matrix):
    canonicalDeg = len(matrix)
    controlMatrix = [''] * (len(matrix[0]) - canonicalDeg)

    # first transform the non einheitsmatrix
    for i in range(len(matrix)):
        k = 0
        for j in range(canonicalDeg, len(matrix[i])):
            controlMatrix[k] = controlMatrix[k] + matrix[i][j]
            k = k + 1
    
    # add the einheitsmatrix
    for i in range(len(controlMatrix)):
        for j in range(len(controlMatrix)):
            char = '1' if i == j else '0'
            controlMatrix[i] = controlMatrix[i] + char
    
    return controlMatrix    

def decode(message, controlMatrix):
    transformedControlMatrix = exercise3.transformMatrix(controlMatrix)
    syndromeClass = exercise3.multiply(message, transformedControlMatrix)
    #print('Detected Syndromeclass: ')
    #print(syndromeClass)
    if syndromeClass != ''.join(['0'] * len(message)):
        for i in range(len(transformedControlMatrix)):
            if transformedControlMatrix[i] == syndromeClass:
                fixedMessage = list(message)
                fixedMessage[i] = '1' if message[i] == '0' else '0'
                message = ''.join(fixedMessage)
        #print('Fixed Encoded Message: ')
        #print(message)   

    einheitsStartIndex = len(controlMatrix[0]) - len(controlMatrix)
    result = message[0:einheitsStartIndex]
    
    return result



def main(m, message, error):
    print('m: ' + str(m))
    controlMatrix = generateControlMatrixFromM(m)
    print('Controlmatrix: ')
    print(controlMatrix)
    generatorMatrix = generateGeneratorMatrix(controlMatrix)
    print('Generatormatrix: ')
    print(generatorMatrix)
    print('Message: ')
    print(message)
    encodedMessage = exercise3.multiply(message, generatorMatrix)
    print('Encoded Message: ')
    print(encodedMessage)
    print('Error: ')
    print(error)
    encodedMessageWithError = f'{int(encodedMessage, 2) ^ int(error, 2):0{len(encodedMessage)}b}'
    print('Encoded Message With Error: ')
    print(encodedMessageWithError)
    controlMatrixOfGeneratorMatrix = generateControlMatrix(generatorMatrix)
    print('Control Matrix from Generator Matrix')
    print(controlMatrixOfGeneratorMatrix)
    decodedMessage = decode(encodedMessageWithError, controlMatrixOfGeneratorMatrix)
    print('Decoded Message: ')
    print(decodedMessage)

def test(m, message, error):
    controlMatrix = generateControlMatrixFromM(m)
    generatorMatrix = generateGeneratorMatrix(controlMatrix)
    encodedMessage = exercise3.multiply(message, generatorMatrix)
    encodedMessageWithError = f'{int(encodedMessage, 2) ^ int(error, 2):0{len(encodedMessage)}b}'
    controlMatrixOfGeneratorMatrix = generateControlMatrix(generatorMatrix)
    decodedMessage = decode(encodedMessageWithError, controlMatrixOfGeneratorMatrix)
    return message==decodedMessage
    

if __name__ == "__main__":
    # main(3,'0101','0010000')
    # main(3,'0101','00100000')
    main(3,'0101','10010000')

    exceptioncase=[]
    workingcase=[]
    notworkingcase=[]

    for q in range(0,50):
        for d in range(0,50):
            for i in range(0,50):
                message = "{0:b}".format(d)
                error = "{0:b}".format(i)
                case=[q,message,error]
                try:
                    if test(q,message,error):
                        workingcase.append(case)
                    else:
                        notworkingcase.append(case)
                except:
                    exceptioncase.append(case)
    
    print(f'Working cases for [matrix, message,error]: {workingcase}, \n\n\n not working cases: {notworkingcase}, \n\n\n exceptional cases: {exceptioncase}')


    