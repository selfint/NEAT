# network.py
# Description : Network class built by Dna object instructions.
# -------------------------------------------------------------

# Graphic Imports
from random import random

from graphviz import Digraph
from typing import Union, Tuple, List

# Project Imports
from dna import Dna, Innovation
from node import HiddenNode, InputNode, OutputNode

# Constants
RENDER_FILE = r'renders/neat-structure.gv'


class Network:

    def __init__(self, inputs: int, outputs: int, weight_range: int, dna: Union[None, Dna] = None, name: str = ''):
        self.inputs = inputs
        self.outputs = outputs
        self.weight_range = weight_range
        self.dna = dna if dna else Dna(self.inputs, self.outputs, self.weight_range)
        self.fitness = 0
        self.nodes = self.dna.node_gene
        self.connections = self.dna.innovation_gene
        self.input_nodes = [node for node in self.nodes if type(node) is InputNode]
        self.output_nodes = [node for node in self.nodes if type(node) is OutputNode]
        self.layers = self.set_layers()
        self.name = name if name else "Network"

    def __str__(self) -> str:
        string = "{}\n".format(self.name)
        for layer in range(len(self.layers)):
            string += "Layer {}\n".format(layer)
            for node in self.layers[layer]:
                string += "\t{}\n".format(node)
                inputs, outputs = self.get_node_connections(node)
                string += "\t\tInput Connections:\n"
                for input_connection in inputs:
                    string += "\t\t\t" + str(input_connection) + "\n"

                string += "\t\tOutput Connections:\n"
                for output_connection in outputs:
                    string += "\t\t\t" + str(output_connection) + "\n"
        return string

    def __repr__(self) -> str:
        return str(self)

    def get_output(self, inputs: list) -> list:
        """
        Calculates the network output.
        :param inputs: Network inputs
        :return: Network output
        """

        # Set the inputs as the network inputs, and reset all other nodes.
        self.initialize_network(inputs)

        # Forward propagate each node's output to all the node it outputs to.
        return self.forward_propagate()

    def initialize_network(self, inputs: list) -> None:
        """
        Resets all nodes and sets the inputs as the inputs of the first layer nodes.
        :param inputs: Network inputs
        :return: None
        """

        # Reset all nodes in the network
        for node in self.nodes:
            node.inputs = []

        # Set each input value as the input to an input node.
        for index in range(len(self.input_nodes)):
            self.input_nodes[index].inputs = [inputs[index]]

    def forward_propagate(self) -> List[float]:
        """
        Tell each node to send its output to each node it is connected to, by layer.
        Assumes that the inputs of the network have been set.
        :return: None
        """

        # Iterate over all layers, and send node outputs in that order.
        for layer in self.layers:
            for node in layer:

                # Calculate node output.
                node.get_output()

                # Get all connections outputting from node.
                _, destination_connections = self.get_node_connections(node)

                for connection in destination_connections:

                    # Send this nodes signal to destination node.
                    destination_node = self.get_node(connection.dst_number)
                    destination_node.inputs.append(node.output)

        # Return the output of all output nodes.
        return [node.get_output() for node in self.output_nodes]

    def get_node_connections(self, node: HiddenNode) -> tuple:
        """
        Returns all connections leading in and out of a node.
        :param node: Node to get connections for
        :return: List of source (in) connections and list of destination (out) connections
        """
        source_connections = [connection for connection in self.connections if connection.dst_number == node.number]
        destination_connections = [connection for connection in self.connections
                                   if connection.src_number == node.number]
        return source_connections, destination_connections

    def add_connection(self, connection: Innovation) -> None:
        """
        Adds a connection to the network.
        :param connection: Connection to add
        :return: None
        """
        self.dna.innovation_gene.append(connection)

    def add_node(self, node: HiddenNode, layer: int, new_layer: bool) -> None:
        """
        Adds a node to the network.
        :param node: Node to add
        :param layer: Node layer
        :param new_layer: Need to create new layer
        :return: None
        """
        node.layer = layer
        self.dna.node_gene.append(node)

        # Create a new layer if needed.
        if new_layer:
            self.layers.insert(layer, [node])

            # Re-assign node numbers
            for layer in range(len(self.layers)):
                for node in self.layers[layer]:
                    node.layer = layer
        else:
            self.layers[layer].append(node)

    def get_node(self, node_number: int) -> HiddenNode:
        """
        Finds a node by its number.
        :param node_number: Number of the node
        :return: Node with correct number
        """
        return [node for node in self.nodes if node.number == node_number][0]

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

    def apply_mutation(self, mutations: list) -> None:
        """
        Applies all configured mutations to the network.
        :param mutations: Configured mutations to add
        :return: None
        """
        for mutation in mutations:

            # Node mutation.
            if len(mutation) == 4:
                node, src, dst, target = mutation
                src_node, dst_node = self.get_node(target.src_number), self.get_node(target.dst_number)

                # Round up node layer.
                node_layer = (src_node.layer + dst_node.layer) / 2.0
                node_layer = int(node_layer + int(target.forward)) \
                    if node_layer % 10.0 >= 0.5 else int(node_layer + int(not target.forward))
                new_layer = node_layer == src_node.layer or node_layer == dst_node.layer
                self.add_node(node, node_layer, new_layer)
                self.add_connection(src)
                self.add_connection(dst)

            # Connection mutation.
            elif len(mutation) == 1:
                innovation, = mutation
                self.add_connection(innovation)

    def crossover(self, mate: 'Network', name: str = '') -> 'Network':
        """
        Performs crossover with another network.
        :param mate: Mate network to perform crossover with
        :return: Child network
        """
        fitter_network = self if self.fitness > mate.fitness else mate if self.fitness < mate.fitness else None
        fitter_dna = fitter_network.dna if fitter_network else None
        child_dna = self.dna.crossover(mate.dna, fitter_dna)
        child = Network(self.inputs, self.outputs, self.weight_range, child_dna, name)
        return child

    def set_layers(self):
        """
        Set each node in its proper layer.
        :return: Set layers.
        """
        layers = {}
        for node in self.nodes:
            if node.layer in layers:
                layers[node.layer].append(node)
            else:
                layers[node.layer] = [node]

        sorted_layers = [[node for node in layers[layer]] for layer in sorted(layers.keys())]
        for layer in range(len(sorted_layers)):
            for node in sorted_layers[layer]:
                node.layer = layer

        return sorted_layers

    def render(self, view: bool = True) -> None:
        """
        Renders the network in 2D.
        :param view: If the render should automatically be viewed
        :return: None
        """

        # TODO find a way to force layers to a certain rank.
        network_graph = Digraph(comment="NEAT structure", strict=True, graph_attr={"rankdir": "LR",
                                                                                   "splines": None})

        # Generate layers
        for layer in range(len(self.layers)):
            with network_graph.subgraph(name=str("Layer {}".format(layer))) as graph_layer:
                rank = "min" if layer == 0 else "max" if layer == (len(self.layers) - 1) else "same"
                graph_layer.attr(rank=rank)

                color = "green" if layer == 0 else "yellow" if layer == (len(self.layers)-1) else "lightgrey"
                for node in self.layers[layer]:
                    graph_layer.node(name=str(node.number),
                                     label='L:' + str(node.layer) + ' N:' + str(node.number),
                                     color=color,
                                     shape="circle", fillcolor=color, style="filled")

        # Generate connections
        for connection in self.connections:
            if connection.enabled:
                color = "red" if connection.weight >= 0 else "blue"
                f = connection.forward
                direction = ' -> ' if f else ' <- '
                src, dst = str(connection.src_number), str(connection.dst_number)
                string = "([Inn. {0}]: {1}{3}{2})".format(connection.number,
                                                          src if f else dst, dst if f else src, direction)
                network_graph.edge(tail_name=str(connection.src_number), head_name=str(connection.dst_number),
                                   color=color, label=string)
        network_graph.render(RENDER_FILE, view=view, cleanup=True)


def configure_mutation(mutations: list, g_innovation_number: int, g_node_number: int) -> tuple:
    """

    Simulates how the main simulation will configure a mutation.
    :param mutations: Mutation list
    :param g_innovation_number: Highest innovation number so far
    :param g_node_number: Highest node number so far
    :return: Configured mutation
    """
    configured_mutations = []

    for mutation in mutations:

        # Node mutation
        if len(mutation) == 4:
            node, src, dst, target = mutation
            node.number = g_node_number
            src.number = g_innovation_number
            src.dst_number = node.number
            dst.src_number = node.number
            target.enabled = False
            dst.number = g_innovation_number + 1
            configured_mutations.append([node, src, dst, target])

            # Increment global counters
            g_innovation_number = g_innovation_number + 2
            g_node_number = g_node_number + 1

        # Innovation mutation
        elif len(mutation) == 1:
            innovation, = mutation
            innovation.number = g_innovation_number
            configured_mutations.append([innovation])

            g_innovation_number += 1

    return configured_mutations, g_innovation_number, g_node_number


def do_mutations(network: Network, g_innovation_number: int, g_node_number: int) -> Tuple[int, int]:
    """
    Mutates the network
    :param g_innovation_number: Highest innovation number so far
    :param g_node_number: Highest node number so far
    :param network: Network to mutate
    :return: Updated global innovation and node numbers
    """
    c_mutations, g_innovation_number, g_node_number = configure_mutation(network.mutate(1, 1, 0, 0),
                                                                         g_innovation_number, g_node_number)
    for c_mutation in c_mutations:
        network.apply_mutation([c_mutation])
    return g_innovation_number, g_node_number


if __name__ == '__main__':
    print('Testing Network')
    network_test = Network(2, 1, 2, name="Parent A")
    network_mate = Network(2, 1, 2, name="Parent B")
    network_test.fitness += 1
    global_innovation_number = len(network_test.connections)
    global_node_number = len(network_test.nodes)
    

    # Test mutations
    for iteration in range(0):
        global_innovation_number, global_node_number = do_mutations(network_test, global_innovation_number,
                                                                    global_node_number)
    for iteration in range(2):
        global_innovation_number, global_node_number = do_mutations(network_mate, global_innovation_number,
                                                                    global_node_number)

    print(network_test)
    # if input("Render Parent A? (y/n) ") == 'y':
    #     network_test.render()

    print(network_mate)
    # if input("Render Parent B? (y/n) ") == 'y':
    #     network_mate.render()

    child = network_test.crossover(network_mate, name="Child")
    print(child)
    print([child.get_output([-1, 0.5]) for _ in range(2)])
    if True or input("Render Child? (y/n) ") == 'y':
        child.render()

