# network.py
# Description : Network class built by Dna object instructions.
# -------------------------------------------------------------


from dna import Dna
from graphviz import Digraph

from node import HiddenNode


class Network:

    def __init__(self, inputs: int, outputs: int, weight_range: int):
        self.inputs = inputs
        self.outputs = outputs
        self.weight_range = weight_range
        self.dna = Dna(self.inputs, self.outputs, self.weight_range)
        self.nodes = self.dna.node_gene
        self.connections = self.dna.innovation_gene
        self.input_nodes = self.dna.node_gene[:self.inputs]
        self.output_nodes = self.dna.node_gene[-self.outputs:]
        self.layers = [self.input_nodes, self.output_nodes]

    def get_output(self, inputs: list) -> list:
        """
        Calculates the network output.
        :param inputs: Network inputs
        :return: Network output
        """

        # Set the inputs as the network inputs, and reset all other nodes.
        self.initialize_network(inputs)

        # Forward propagate each node's output to all the node it outputs to.
        self.forward_propagate()

        # Get all output node's output.
        return [node.get_output() for node in self.output_nodes]

    def initialize_network(self, inputs: list) -> None:
        """
        Resets all nodes and sets the inputs as the inputs of the first layer nodes.
        :param inputs: Network inputs
        :return: None
        """

        # Set each input value as the input to an input node.
        for index in range(self.input_nodes):
            self.input_nodes[index].inputs = list(inputs[index])

    def forward_propagate(self) -> None:
        """
        Tell each node to send its output to each node it is connected to, by layer.
        :return: None
        """

    def add_node(self, node: HiddenNode, layer: int, new_layer: bool) -> None:
        """
        Adds a node to the network.
        :param node: Node to add
        :param layer: Node layer
        :param new_layer: Need to create new layer
        :return: None
        """
        self.dna.node_gene.append(node)

        # Create a new layer if needed.
        if new_layer:
            self.layers.insert(layer, node)
        else:
            self.layers[layer].append(node)

    def mutate(self, node_mutation_rate: float, innovation_mutation_rate: float,
               weight_mutation_rate: float, random_weight_rate: float) -> list:
        """
        Can mutate the genome by adding a node mutation or a connection mutation, and it might also mutate a weight.
        :param node_mutation_rate: Probability for a node mutation
        :param innovation_mutation_rate: Probability for a node mutation
        :param weight_mutation_rate: Probability for a node mutation
        :param random_weight_rate: Probability for a weight to be changed to a totally random value,
                                   instead of being perturbed
        :return: All mutations that occurred
        """
        return self.dna.mutate(node_mutation_rate, innovation_mutation_rate, weight_mutation_rate, random_weight_rate)

    def render(self) -> None:
        """
        Renders the network in 2D.
        :return: None
        """
        network_graph = Digraph(comment="NEAT structure")
        for node in self.nodes:
            network_graph.node(name=str(node.number), label=str(node), color="green")
        for connection in self.connections:
            network_graph.edge(tail_name=str(connection.src_number), head_name=str(connection.dst_number),
                               label="{:.2f}".format(connection.weight))
        network_graph.render('renders/neat-structure.gv', view=True)


def configure_mutation(mutations: list, global_innovation_number: int, global_node_number: int) -> list:
    """

    Simulates how the main simulation will configure a mutation.
    :param mutations: Mutation list
    :param global_innovation_number: Highest innovation number so far
    :param global_node_number: Highest node number so far
    :return: Configured mutation
    """

    for mutation in mutations:

        # Node mutation
        if len(mutation) == 4:
            node, src, dst, target = mutation

        # Innovation mutation
        elif len(mutation) == 1:
            innovation, = mutation


if __name__ == '__main__':
    print('Testing Network')
    network_test = Network(2, 3, 2)
    network_test.render()

