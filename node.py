# node.py
#
# Description : All node types, Input, Hidden or Output.
# ------------------------------------------------------

# Imports
from math import e


# String representation
STRING = "{}: {}"


# Default activation function
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + pow(e, -4.9 * x))


class HiddenNode:

    def __init__(self, number: int, layer: int, activation=sigmoid):
        self.number = None if number == -1 else number
        self.activation = activation
        self.layer = layer
        self.inputs = []
        self.output = 0

    def get_output(self) -> float:
        """
        Calculates the output of this node, which is equal to the activation of the sum of its inputs.
        :return: Node output
        """
        self.output = self.activation(sum(self.inputs))
        return self.output

    def __repr__(self):
        return STRING.format(self.name(), self.number)

    def __str__(self):
        return repr(self)

    def name(self) -> str:
        """
        Returns the name of the class.
        :return: Class name
        """
        return self.__class__.__name__


class InputNode(HiddenNode):

    def __init__(self, number: int, layer: int):

        # The lambda function replaces the activation function so that the output of an input node
        # is only the sum of its inputs, without activation.
        super(InputNode, self).__init__(number, layer, lambda x: x)


class OutputNode(HiddenNode):

    def __init__(self, number: int, layer: int, activation=sigmoid):
        super(OutputNode, self).__init__(number, layer, activation)


if __name__ == '__main__':
    print('Testing Nodes')
    input_test = InputNode(0, 0)
    hidden_test = HiddenNode(1, 1)
    output_test = OutputNode(2, 2)
    print(input_test, hidden_test, output_test)
    print(input_test.get_output(), hidden_test.get_output(), output_test.get_output())
