# dna.py
#
# Description : Genome containing instruction on how to build a network.
# ----------------------------------------------------------------------

# General imports
from random import choice, random
from typing import Tuple, List

# Project imports
from functions import ignore
from innovation import Innovation
from node import *


class Dna:

    node_gene: List[HiddenNode]

    def __init__(self, inputs: int, outputs: int, weight_range: int, empty=False):
        self.inputs = inputs
        self.outputs = outputs
        self.weight_range = weight_range
        self.empty = empty

        # Generate input and output nodes, if not empty
        self.node_gene = [InputNode(node_number, 0) if node_number < self.inputs else OutputNode(node_number, 1)
                          for node_number in range(self.inputs + self.outputs)] if not self.empty else []
        self.input_nodes = self.node_gene[:self.inputs]
        self.output_nodes = self.node_gene[-self.outputs:]

        # Fully connect input and output genes, if not empty
        self.innovation_gene = []
        if not self.empty:
            for input_node in self.input_nodes:
                for output_node in self.output_nodes:
                    self.innovation_gene.append(Innovation(len(self.innovation_gene),
                                                           input_node.number,
                                                           output_node.number,
                                                           self.random_weight(),
                                                           True, True))

    def random_weight(self) -> float:
        """
        Generates a random weight value.
        :return: Weight value
        """
        return random() * self.weight_range * 2 - self.weight_range

    def get_number_node(self, number: int) -> HiddenNode:
        """
        Returns a node by its node number.
        :param number: Node number of the node
        :return: Node with corresponding number
        """
        node = [node for node in self.node_gene if node.number == number]

        # Raise index error if node not in dna node gene.
        if not node:
            raise IndexError('Node number {} is not in dna.'.format(number))
        return node[0]

    def get_nodes(self, node_type: type, *other_types) -> List[HiddenNode]:
        """
        Gets all node of a type (or types) for node gene.
        :return: list of nodes
        """
        return [node for node in self.node_gene if type(node) is node_type or type(node) in other_types]

    def new_innovation(self, src_number: int, dst_number: int) -> Tuple[Innovation]:
        """
        Generates a new innovation gene and adds it to the dna.
        :param src_number: Source node's number.
        :param dst_number: Destination node's number.
        :return: New innovation
        """
        forward = self.get_number_node(src_number).layer < self.get_number_node(dst_number).layer
        new_innovation = Innovation(-1, src_number, dst_number, self.random_weight(), True, forward)
        return new_innovation,

    def new_node(self, target_innovation: Innovation) -> Tuple[HiddenNode, Innovation, Innovation, Innovation]:
        """
        Generates a new node that 'splits' an existing an innovation and generates two new ones.
        One leads into the node with weight 1 and the other lead out of the node with the target
        innovation's weight. The new node's number and the two new innovations numbers will have
        to be set by the main simulation. The target innovation will also need to be disabled by
        the main simulation.
        :param target_innovation: Innovation to split
        :return: The new node, the two new innovations, and the old innovation to disable
        """
        src_node = self.get_number_node(target_innovation.src_number)
        dst_node = self.get_number_node(target_innovation.dst_number)
        new_node = HiddenNode(None, None)
        forward = src_node.layer < dst_node.layer
        new_source_innovation = Innovation(None, src_node.number, new_node.number, 1, True, forward)
        new_destination_innovation = Innovation(None, new_node.number, dst_node.number, target_innovation.weight,
                                                True, forward)
        return new_node, new_source_innovation, new_destination_innovation, target_innovation

    def get_available_connections(self) -> List[Tuple[int, int]]:
        """
        Finds all possible source and destination node pairs that are not connected.
        :return: List of source and destination node numbers
        """

        all_connections = [(innovation.src_number, innovation.dst_number) for innovation in self.innovation_gene]

        available_connections = []
        for src_node in self.node_gene:
            for dst_node in ignore(self.node_gene, *self.input_nodes):
                avenue = src_node.number, dst_node.number
                if avenue not in all_connections:
                    if type(src_node) is HiddenNode:
                        available_connections.append(avenue)
                    elif type(src_node) is not type(dst_node):
                        available_connections.append(avenue)

        return available_connections

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

        mutations = []

        # Node mutation
        if random() < node_mutation_rate:
            target_innovation = choice(self.innovation_gene)
            mutations.append(self.new_node(target_innovation))

        # Connection mutation
        if random() < innovation_mutation_rate:
            available_connections = self.get_available_connections()
            if available_connections:
                src_number, dst_number = choice(available_connections)
                mutations.append(self.new_innovation(src_number, dst_number))

        # Mutate a weight
        if random() < weight_mutation_rate:
            innovation = choice(self.innovation_gene)

            # Mutate the weight either by completely changing it, or slightly perturbing it
            if random() < random_weight_rate:
                innovation.weight = random() * self.weight_range * 2 - self.weight_range
            else:
                innovation.weight += random() * self.weight_range / 8.0

        return mutations

    def crossover(self, mate: 'Dna', fitter_parent: object) -> 'Dna':
        """
        Generates a child dna based of mate and self dna.
        :param mate: Mate's dna
        :param fitter_parent: Which parent has the higher fitness
        :return: Child's dna
        """

        def sort_innovations(a_innovations: list, b_innovations: list) -> tuple:
            """
            Sorts innovations from both parents into matching, a-specific and b-specific innovations lists.
            :param a_innovations: Parent A's innovations
            :param b_innovations: Parent B's innovations
            :return: Matching innovations, non-matching innovations
            """
            ab_matching, a_specific, b_specific = [], [], []

            # Check for innovations present in both parents, and innovations present only in parent A.
            for a_innovation in a_innovations:
                if a_innovation in b_innovations:
                    ab_matching.append(a_innovation)
                else:
                    a_specific.append(a_innovation)

            # Check for innovations present only in parent B.
            for b_innovation in b_innovations:
                if b_innovation not in a_innovations:
                    b_specific.append(b_innovation)

            return ab_matching, a_specific, b_specific

        # Initialize child dna as empty dna.
        child_dna = Dna(self.inputs, self.outputs, self.weight_range, empty=True)

        # Get pointers to nodes and innovations
        child_nodes = child_dna.node_gene
        child_innovations = child_dna.innovation_gene

        # Get sorted innovations.
        matching, self_specific, mate_specific = sort_innovations(self.innovation_gene, mate.innovation_gene)

        # Matching genes are inherited randomly.
        for innovation in matching:
            if random() < 0.5:
                child_innovations.append(innovation)

        # Non matching genes (A.K.A. disjoint and excess genes) are inherited from the fitter parent.
        if self is fitter_parent:
            child_innovations.extend(self_specific)
        elif mate is fitter_parent:
            child_innovations.extend(mate_specific)

        # If both parents have equal fitness (unlikely, but possible).
        else:
            for innovation in self_specific + mate_specific:
                if random() < 0.5:
                    child_innovations.append(innovation)

        # Add all necessary nodes to child.
        nodes = set()
        for child_innovation in child_innovations:
            nodes.add(child_innovation.src_number)
            nodes.add(child_innovation.dst_number)

        # Add all input and output nodes (if they were missed in crossover).
        for node in self.get_nodes(InputNode, OutputNode) + mate.get_nodes(InputNode, OutputNode):
            nodes.add(node.number)

        # Add all necessary nodes to child dna.
        for node in nodes:

            # Check if the node is in either parent.
            for parent in (self, mate):

                # If node is not in self then it will be in mate.
                try:
                    child_node = parent.get_number_node(node)

                    if child_node not in child_nodes:
                        child_nodes.append(child_node)

                        # If node is in self then we can skip over mate, node has already been added.
                        break

                except IndexError:
                    continue

        return child_dna


if __name__ == '__main__':
    print('Testing Dna')
    dna_test = Dna(4, 3, 2)
    dna_mate = Dna(4, 3, 2)
    innovation_mutation = dna_test.new_innovation(2, 4)
    node_mutation = dna_test.new_node(dna_test.innovation_gene[0])
    child = dna_test.crossover(dna_mate, None)
    print(child.node_gene)
    print(child.innovation_gene)
    print(len(child.innovation_gene))
