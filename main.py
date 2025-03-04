from sympy import Matrix
import matplotlib.pyplot as plt
import numpy as np

points = ...

def readData():
    points = []
    
    
    with open('data/data1.txt', 'r') as file:
        for line in file:
            data = line.strip().split(",")
            
            points.append((float(data[0]), float(data[1])))
            
        
    return points
        
    
def getPoints():
    xVals = []
    points = []
    
    print("Getting Points From User (Enter q to end)")
    while True:
        x = input("Enter X Value: ")
        
        if x == "q":
            break
        xVals.append(int(x))
    
    for x in xVals:
        yVal = input(f"Enter Y Value for X = {x}: ")
        points.append((x, float(yVal) ))


    return points

def makeMatrix(points):
    y = []
    x = []
    b = [[i] for i in range(len(points))]
    
    for i in points:
        x.append([1, i[0]])
        y.append([i[1]])
    
    return y, x, b

def transpose(mat):
    rows = len(mat)
    cols = len(mat[0])
    
    result = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for i in range(rows):  
        for j in range(cols):  
            result[j][i] = mat[i][j]  
            
    return result  

def getMenu():
    print("\n\n- - - Menu - - - \n")
    print("1. Enter your own Points")
    print("2. Use Default Points")
    
    while True:
        userInput = int(input("Enter 1 or 2: "))
        if userInput == 1 or userInput == 2:
            break
    
    return userInput

def matCombine(a,b):
    return [row + [b[i][0]] for i, row in enumerate(a)]


def matMult(a,b):
    if len(a[0]) != len(b):
        print("Cols of matrix A must equal Rows of matrix B")
        return 
    
    
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] = result[i][j] + (a[i][k] * b[k][j])
            
    return result

def plotPoints(points):
    for point in points:
        plt.scatter(point[0], point[1])
    
    
def plotLine(yInt, slope):
    x = np.linspace(0, 10000, 400)
    y = slope * x + yInt
    plt.plot(x, y, linewidth=2.5, color = "Red") 

    
def rrref(mat):
    mat = Matrix(mat)
    return mat.rref()

def calcError(a,b):
    mat = [a[i][0] - b[i][0] for i in range(len(a))]  
    result = sum(x**2 for x in mat)  
    return result**(1/2)  
            

def run():
    #userIn = getMenu()
    
    #if False:
    #    points = getPoints()
        
    points = readData()
    
    yMat, xMat, bMat = makeMatrix(points)
    
    xTrans = transpose(xMat)
    xTransX = matMult(xTrans, xMat)
    xTransY = matMult(xTrans, yMat)
    
    xTransxWithxTransB = matCombine(xTransX, xTransY)
    rowReduced, poivits = rrref(xTransxWithxTransB)
    yIntercept, slope = rowReduced[0,2], rowReduced[1, 2]
    
    xMatResult = matMult(xMat, [[yIntercept], 
                                [slope]])
    
    error = calcError(yMat, xMatResult)
    print(f"\nyMat: {yMat},\nxMat: {xMat},\nbMat: {bMat}")
    print(f"\nxTrans: {xTrans}")
    print(f"\nxTransX: {xTransX}\nxTransY: {xTransY}")
    print(f"\nxTransxWithxTransB: {xTransxWithxTransB}")
    print(f"\nRow Reduced {rowReduced}")
    print(f"\nxMatResult: {xMatResult[0]}")
    print(f"\nLinear Reg line is: y = {round(yIntercept,2)} + {round(slope,2)}x")
    print(f"\n\nError = {error}")
    print("\n")
    print("\n")
    
    expected_y = [140 + x[0] for x in points]
    computed_y = [xMatResult[i][0] for i in range(len(xMatResult))]

    error_check = sum((expected_y[i] - computed_y[i])**2 for i in range(len(expected_y)))**(1/2)
    print(f"Error compared to ideal line: {error_check}")
    
    # Plotting
    fig, ax = plt.subplots()
    plotPoints(points)
    plotLine(yIntercept, slope)

    plt.xlim(0,10000)
    plt.ylim(0,10000)

    plt.title(f"y = {round(yIntercept,2)} + {round(slope,2)}x \nError: {round(error,2)}")
    plt.xlabel("X Vals")
    plt.ylabel("Y Vals")
    plt.show()
if __name__ == "__main__":
    run() 