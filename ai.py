from numpy import exp, array, random, dot
import math

class Connection():
    def __init__(self):
        self.weight=0
        self.neuron=False
   
    def updateWeight(self):
        self.weight+=1

    def deupdateWeight(self):
        self.weight-=1

    def setNeuron(self, neuron):
        self.neuron=neuron
        
    def getWeight(self):
        return self.weight

class Neuron():

    def __init__(self):
        self.weight=0
        self.fired=False
        self.value=""
        self.connections=[]
    
    def addConnection(self, connection):
        conex=Connection()
        conex.setNeuron(connection)
        self.connections.append(conex)
        
    def addSubConnection(self, n, connection):
        if len(self.connections) > n:
           if isinstance(self.connections[n], list) == True: 
                conex=Connection()
                conex.setNeuron(connection)
                self.connections[n].append(conex)

    def setValue(self, v):
        self.value=v

    def setWeight(self, w):
        self.weight=w
        
    

    def getConnection(self, n):
        return self.connections[n]

    def getSubConnection(self, n, i):
        N1=self.connections[n]
        return N1[i]

    def updateWeight(self):
        self.weight+=1

    def getWeight(self):
        return self.weight
    
    def findMinWeight(self):
        minDeath=81
        for n in range(len(self.connections)):
            w=self.connections[n].getWeight()
            if w < minDeath:
                minDeath=w
        return minDeath

    def findMaxWeight(self):
        maxDeath=0
        for n in range(len(self.connections)):
            w=self.connections[n].getWeight()
            if w > maxDeath:
                maxDeath=w
        return maxDeath

    def findMeanWeight(self):
        count=0
        mean=0
        for n in range(len(self.connections)):
            w=self.connections[n].getWeight()
            if w > 0:
                mean+=w
                count+=1
        if count > 1:
            mean//=count
        return mean
    
    def splitConnections(self, n):
        for i in range(n):
            self.connections.append([])
        
output=[]
middle=[]
input_layer=[]
inputs=[]


def guess(gue):
    guesses_vector=[]
    for i in range(len(gue)):
        
        C1=middle[gue[i][0]-18]
        C1.updateWeight()

        C2=input_layer[1].getSubConnection(gue[i][1],gue[i][0]- 18)
        C2.updateWeight()
     
        C3=input_layer[2].getSubConnection(gue[i][2],gue[i][0] - 18)
        C3.updateWeight()
        
        guesses = 0;
        
        for n in range(18, 81):
            y = predict(gue[i])
            guesses+=1
            if int(y) != int(gue[i][3]):
                PN=middle[gue[i][0]-18].getConnection(int(y)-18)
                PN.deupdateWeight()
            else:
                break
                
        guesses_vector.append(guesses)
        

       # print("Guesses took")
       # for i in range(len(guesses_vector)):
        #     print(guesses_vector[i])
        

    for i in range(len(guesses_vector)):
        if guesses_vector[i] > 2:
            guesses_vector=[]
            guess(gue)
            break
        
    
def show_guesses(gue):
    for i in range(len(gue)):
        y=predict(gue[i])
        print("Predicted death age of: " + y)
        print ("For the person with an age of " + str(gue[i][0]))
        if gue[i][1] == 1:
            print("Male")
        else:
            print("Female")
        if gue[i][2] == 1:
            print("Smokes")
        else:
            print("Doesn't smoke")
        print('\n')
    

def train(inp):
    for i in range(len(inp)):
        C1=middle[inp[i][0]-18]
        C1.updateWeight()

        C2=input_layer[1].getSubConnection(inp[i][1],inp[i][0]- 18)
        C2.updateWeight()
     
        C3=input_layer[2].getSubConnection(inp[i][2],inp[i][0] - 18)
        C3.updateWeight()

        C4=middle[inp[i][0]-18].getConnection(inp[i][3]-18)
        C4.updateWeight()


def predict(y):
    M1=middle[y[0]-18]
    M1SX=input_layer[1].getSubConnection(y[1],y[0]-18)
    M1SS=input_layer[2].getSubConnection(y[2],y[0]-18)
    wM1=M1.getWeight()
    wM1SX=M1SX.getWeight()
    wM1SS=M1SS.getWeight()
    DeathMin=M1.findMinWeight()
    DeathMax=M1.findMaxWeight()
    DeathMean=M1.findMeanWeight()

    
    for index in range(y[0]-18, len(M1.connections)):
            W=M1.connections[index].getWeight()
            x=y[0]
            if DeathMean <= W:
                 x = str(index+18)
                 break;            
    return x
                    
            
    print(wM1,wM1SX, wM1SS,DeathMin,DeathMax,DeathMean)



for i in range(18, 81):
    N1=Neuron()
    N1.setValue(str(i))
    N2=Neuron()
    N2.setValue(str(i))
    middle.append(N1)
    output.append(N2)



#second paramter is sex 0 female
#                       1 male
#third paramter is smoker  0 no
#                          1 yes

guess_array = [ [32, 1, 1 ,60],
                [43, 0, 1, 52],
                [25, 0, 0, 77],
                [30,1,1,44],
                [20,1,0,75],
                [41,0,0,77],
                [42,1,1,55],
                [44,1,1,55],
                [45,0,1,57],
                [46,0,0,73]
                ]
inputs = [  [ 55, 0, 1, 78],
         [ 34, 1, 0, 66],
         [ 44, 1, 1, 55],
         [ 20, 0, 0, 75],
         [ 30, 1, 0, 78],
         [ 20, 0, 1, 34],
         [ 46, 1, 1, 60]
                         ]

for x1 in range(len(middle)):
    N1=middle[x1]
    for x2 in range(len(output)):
        N1.addConnection(output[x2])

for n in range(0,3):
    x=Neuron()
    input_layer.append(x)


input_layer[1].splitConnections(2)
input_layer[2].splitConnections(2)

for x in range(len(middle)):
    input_layer[0].addConnection(middle[x])
    input_layer[1].addSubConnection(0,middle[x])
    input_layer[1].addSubConnection(1,middle[x])
    input_layer[2].addSubConnection(0,middle[x])
    input_layer[2].addSubConnection(1,middle[x])

train(inputs)
guess(guess_array)
show_guesses(guess_array)


