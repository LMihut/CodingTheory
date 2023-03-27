def generateRMGeneratorMatrix(r, m):
    # all cases for r and m comparison
    if r > m:
        r = m
    
    if r != 0 and m != 0:
        g1 = generateRMGeneratorMatrix(r, m - 1)
        g2 = generateRMGeneratorMatrix(r - 1, m - 1)
    elif r == 0:
        return ['1' * pow(2, m)]

    g1Matrix = [''] * len(g1)
    g2Matrix = [''] * len(g2)
    for i in range(len(g1)):
        g1Matrix[i] = ''.join(g1[i]) + ''.join(g1[i])
    for i in range(len(g2)):
        g2Matrix[i] = '0' * pow(2, m - 1) + ''.join(g2[i])
    
    return g1Matrix + g2Matrix


def main(r,m):
    rmGeneratorMatrix = generateRMGeneratorMatrix(r, m)
    print('Generator Matrix of RM(' + str(r) + ',' + str(m) + '):')
    print(rmGeneratorMatrix)

def test(r,m):
    rmGeneratorMatrix = generateRMGeneratorMatrix(r, m)

if __name__ == "__main__":
    # main(1,3)
    # main(2,5)
    # main(3,4)
    main(3,3)
    # main(2,6)
    # main(1,7)

    exceptioncase=[]
    workingcase=[]

    for i in range(0,50):
        for j in range(0,50):
            case=[i,j]
            try:
                test(i,j)
                workingcase.append(case)
            except:
                exceptioncase.append(case)
    
    print(f'Working cases for [r,m]: {workingcase}, \n\n\n not working cases: {exceptioncase}')
