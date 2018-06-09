"""
node.py

Description: Node object is a node for the network.py object.
"""

# Imports

# Constants

class Node(object):

    def __init__(self, innovation_number):
        """
        __init__(self, innovation_number) --> Node

        This function builds a Node object, and gives it an innovation number.
        """
        super(Node, self).__init__()
        
        # NEAT algorithm
        self.innovation_number = innovation_number
        self.inputs = {}
        
        # Regular neural network algorithm
        self.output = 0
        
    def send_output(self, output_node, weight):
        """
        send_output(self, output_node, weight) --> None

        This function sends the nodes output times weight into output_node.
        """
        output_node.inputs[self] = self.output * weight

    def get_output(self):
        """
        get_output(self) --> float

        This function calculates the output of a node as the sum of it's inputs.
        """
        self.output = sum(self.inputs.values())
        return self.output