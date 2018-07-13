"""
innovation.py

--- Description ---
Innovation object for dna.
An innovation node genes and connection genes for NEAT compatible network.
Innovation:
    Node Genes:
        • node number
        • node type

    Connection Genes:
        • connection input node number
        • connection ouput node number
        • connection weight
        • connection state (enabled/disabled)
        • innovation number

Node:
    Node genes are the topology of the network. Node genes do not have an innovation 
    number. When crossover is performed, node genes of the mate are simply extend with
    source node genes.

    Example:
        Node Genes source:
            Node 1
            Input node
            
            Node 2
            Output node
        
        Node Genes mate:
            Node 1
            Input node
            
            Node 2
            Output node
            
            Node 3
            Hidden node

        Crossover:
            Node 1
            Input node
            
            Node 2
            Output node
            
            Node 3
            Hidden node

Connection:
    Connections genes are the weights of the network. Each connection has a source
    and a destination, that show the direction in which they send the output of a node into
    the input of the next node. The weight is multiplied by the node output. A connection
    can also be disabled, so that no signals are sent by it. Innovation numbers determine
    how crossover is handled. 
    
    If an innovation is unique, meaning only one network has it, the child will get this
    innovation, only if the parent with the innovation has the higher fitness (Randomly
    determined if both fitnesses are identical).
    
    If both parents have the same innovation the child 
"""