""" 
neat.py

Description: Neat object is a neural network that is built according to the NEAT formula.
             Using innovations as instructions.
"""

# Imports
from node import Node

# Constants
NETWORK_INPUT = 0

class Neat(object):

    def __init__(self, inputs, outputs):
        super(Neat, self).__init__(self)
        self.inputs = inputs
        self.outputs = outputs
        self.innovations = {}
        self.connections = {}
        self.nodes = []
        self.input_nodes = []
        self.output_nodes = []

        # Genearte network nodes
        for i in xrange(self.inputs):
            new_node = Node(i)
            self.innovations[i] = new_node
            self.nodes.append(new_node)
            self.input_nodes.append(new_node)
    
    def get_output(self, inputs):
        """
        get_output(self, inputs) --> list

        This function activates each node once. Returns the outputs of the output nodes.
        """
    
    def set_input(self, inputs):
        for node, net_input in self.inputs, inputs:
            node.inputs[NETWORK_INPUT] = net_input
