# Pseudocode from https://en.wikipedia.org/wiki/Row_echelon_form#Pseudocode_for_reduced_row_echelon_form
def generateCanonicalGeneratorMatrix(matrix):
    lead = 0
    rowCount = len(matrix)
    columnCount = len(matrix[0])

    for r in range(rowCount):
        if columnCount <= lead:
            return matrix
        i = r
        while matrix[i][lead] == '0':
            i = i + 1
            if rowCount == i:
                i = r
                lead = lead + 1
                if columnCount == lead:
                    return matrix
        if i != r:
            tmpRow = matrix[i]
            matrix[i] = matrix[r]
            matrix[r] = tmpRow

        rLeadValue = matrix[r][lead]
        matrix[r] = ''.join([(str(int(int(rowValue, 2) / int(rLeadValue, 2)) % 2)) for rowValue in matrix[r]])
        for j in range(rowCount):
            if j != r:
                jLeadValue = matrix[j][lead]
                matrix[j] = ''.join([(str((int(jValue, 2) ^ (int(jLeadValue, 2) * int(rValue, 2))))) for rValue, jValue in zip(matrix[r], matrix[j])])

        lead = lead + 1
    return matrix

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

def transformMatrix(matrix):
    transformedMatrix = [''] * len(matrix[0])

    for i in range(len(matrix)):
        k = 0
        for j in range(len(matrix[i])):
            transformedMatrix[k] = transformedMatrix[k] + matrix[i][j]
            k = k + 1

    return transformedMatrix

def generateSyndromeTable(matrix):
    transformedMatrix = transformMatrix(matrix)

    amountOfSyndromeClasses = pow(2, len(matrix))
    syndromeTable = {}
    syndromeTable['0' * len(matrix[0])] = '0' * len(transformedMatrix[0])

    for i in range(1, len(matrix[0])):
        binaryErrorType = f'{i:0{len(matrix[0])}b}'
  
        for _ in range(len(matrix[0])):
            syndromeClass = multiply(binaryErrorType, transformedMatrix)
            
            # check whether the syndromClass was already calculated
            if syndromeClass not in syndromeTable.values():
                syndromeTable[binaryErrorType] = syndromeClass

            # check whether all syndromClasses have been found
            if amountOfSyndromeClasses == len(syndromeTable):
                return syndromeTable

            # shift the binaryErrorType and check whether we are still searching for a valid errorType
            binaryErrorType = f'{int(binaryErrorType, 2) << 1:0{len(matrix[0])}b}'[-len(matrix[0]):]
            if binaryErrorType.find('1') == -1:
                break

    # if matrix is empty fallback
    return syndromeTable

def multiply(x, y):
    product = ''.join(['0'] * len(y[0]))
    for i in range(len(x)):
        if x[i] == '1':
            product = f'{int(product, 2) ^ int(y[i], 2):0{len(y[0])}b}'
    return product

def getErrorVectorFromSyndromeClass(syndromeTable, syndromeClass):
    for vector, sClass in syndromeTable.items():
        if sClass == syndromeClass:
            return vector

def decode(message, controlMatrix, error, syndromeTable):
    syndromeClass = multiply(message, transformMatrix(controlMatrix))
    if syndromeClass != '0' * len(syndromeClass):
        errorVector = getErrorVectorFromSyndromeClass(syndromeTable, syndromeClass)
        #print('Detected Syndromeclass: ')
        #print(errorVector + ': ' + syndromeClass)
        fixedEncodedMessage = f'{int(message, 2) ^ int(error, 2):0{len(errorVector)}b}'
        #print('Fixed Encoded Message: ')
        #print(fixedEncodedMessage)
        message = fixedEncodedMessage

    einheitsStartIndex = len(controlMatrix[0]) - len(controlMatrix)
    result = message[0:einheitsStartIndex]
    
    return result


def main(matrix,message='11',error='00100'):
    print('Generator Matrix')
    print(matrix)
    canonicalGeneratorMatrix = generateCanonicalGeneratorMatrix(matrix)
    print('Canonical Generator Matrix: ')
    print(canonicalGeneratorMatrix)
    controlMatrix = generateControlMatrix(canonicalGeneratorMatrix)
    print('Control Matrix: ')
    print(controlMatrix)
    syndromeTable = generateSyndromeTable(controlMatrix)
    print('Syndrome Table: ')
    print(syndromeTable)
    message = '11'
    print('Message: ')
    print(message)
    encodedMessage = multiply(message, canonicalGeneratorMatrix)
    print('Encoded Message: ')
    print(encodedMessage)
    error = '00100'
    print('Error: ')
    print(error)
    encodedMessageWithError = f'{int(encodedMessage, 2) ^ int(error, 2):0{len(encodedMessage)}b}'
    print('Encoded Message With Error: ')
    print(encodedMessageWithError)
    decodedMessage = decode(encodedMessageWithError, controlMatrix, error, syndromeTable)
    print('Decoded Message: ')
    print(decodedMessage)

def test(matrix,message='11',error='00100'):
    canonicalGeneratorMatrix = generateCanonicalGeneratorMatrix(matrix)
    controlMatrix = generateControlMatrix(canonicalGeneratorMatrix)
    syndromeTable = generateSyndromeTable(controlMatrix)
    encodedMessage = multiply(message, canonicalGeneratorMatrix)
    encodedMessageWithError = f'{int(encodedMessage, 2) ^ int(error, 2):0{len(encodedMessage)}b}'
    decodedMessage = decode(encodedMessageWithError, controlMatrix, error, syndromeTable)
    return message == decodedMessage
    


if __name__ == "__main__": 
    # main(['01111', '10101'])
    # main(['011111', '101011'])
    # main(['0111111', '1010111'])
    # main(['101111', '110101'])

    exceptioncase=[]
    workingcase=[]
    notworkingcase=[]

    for i in range(0,50):
        for j in range(0,50):
            for k in range(0,50):
                for l in range(0,50):
                    message = "{0:b}".format(k)
                    error = "{0:b}".format(l)
                    matrix=["{0:b}".format(i),"{0:b}".format(j)]
                    case=[matrix,message,error]
                    try:
                        if test(matrix,message,error):
                            workingcase.append(case)
                        else:
                            notworkingcase.append(case)
                        
                    except:
                        exceptioncase.append(case)
        
    print(f'Working cases for [matrix, message,error]: {workingcase}, \n\n\n not working cases: {notworkingcase}, \n\n\n exceptional cases: {exceptioncase}')
    
