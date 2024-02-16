import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(3,2)
        self.weights = self.weights * 2 - 1

    def Evaluate(self, mode):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()

        # Construct the command string, including self.myID
        command = "start /B python simulate.py " + mode + " " + str(self.myID)

        # Optional: Print the command for verification
        print(command)  # Uncomment this line for debugging

        # Execute the command
        os.system(command)

        fitnessFile = open("fitness.txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-3, 3, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[-0.5, 0, 1.0])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[0.5, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=3, weight=1.0)
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=3, weight=1.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=1.0)
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=1.0)
        for currentRow in range(self.weights.shape[0]):
            for currentColumn in range(self.weights.shape[1]):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + 3, weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1


    def Set_ID(self):
        self.myID

