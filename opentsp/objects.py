import math  # Node, Edge, Instance
import numpy  # Node, Path, Instance
import matplotlib.pyplot as plt  # Node, Edge, Path, Instance
import itertools  # Instance, Solver
from opentsp import reducers  # Instance
import csv  # Generator
import time  # Solver
from collections.abc import Sequence  # Path


class Node:
    """Represents the nodes as points with a position x, y.
    The density attribute is used later on, if desired, and is related to the position of a node within a TSP instance.
    """
    test = False

    def __init__(self, x=0, y=0, density=None):
        """Create a new node at x, y."""
        self.x = x
        self.y = y
        self.density = density

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def random_node(lower=0, upper=100):
        node = Node(numpy.random.randint(lower, upper), numpy.random.randint(lower, upper))
        return node

    def dist_from_other(self, other):
        return math.hypot((self.x - other.x), (self.y - other.y))

    def scatter(self):
        """Uses plot.scatter to place an individual node on a graph. Make sure to set the xlim and ylim parameters of
        the plot before running plot.show."""
        if Node.test is True:
            plt.xlim(xmin=0, xmax=100)
            plt.ylim(ymin=0, ymax=100)
            plt.scatter(self.x, self.y)
            plt.show()
        else:
            plt.scatter(self.x, self.y)


class Edge:
    """Represents the edges as having a length and being bounded by two points."""
    test = False

    def __init__(self, node_one, node_two, length=None, directed=False, angle=0, fitness='good', weight=0):
        """Create an edge consisting of two node objects."""
        self.node_one = node_one
        self.node_two = node_two
        self.directed = directed
        self.length = length
        self.angle = angle
        self.fitness = fitness
        self.weight = weight

    def __str__(self):
        return f"({self.node_one}, {self.node_two}, {self.length}, {self.directed}, {self.angle}, {self.fitness}, " \
               f"{self.weight})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        """Equality depends on whether an edge is directed or not.
        Undirected edges are considered equal if they have the same two nodes, regardless of position.
        Directed edges are considered equal only if the nodes are in the same position."""
        if self.directed is False:
            if self.node_one == other.node_one and self.node_two == other.node_two or \
                    self.node_one == other.node_two and self.node_two == other.node_one:
                return True
            else:
                return False

        elif self.directed is True:
            if self.node_one == other.node_one and self.node_two == other.node_two:
                return True
            else:
                return False

    def __lt__(self, other):
        """It is implied that an edge is less than another edge if the length of the first is greater than the length
        of the second."""
        if self.length_ < other.length_:
            return True

    @property
    def length_(self):
        if self.length is None:
            self.length = math.hypot((self.node_one.x - self.node_two.x), (self.node_one.y - self.node_two.y))
            return self.length
        else:
            return self.length

    @property
    def midpoint(self):
        return Node((self.node_one.x + self.node_two.x)/2, (self.node_one.y + self.node_two.y)/2)

    @property
    def indiv_nodes_as_list(self):
        return [self.node_one, self.node_two]

# TODO: write an individual rank property for an edge, returning it's combined rank from each connected node

# TODO: write a function to check if an edge is crossed by another edge

    def plot(self, show_nodes=False, color='b', edge_width=0.5, zorder=-1):
        plt.xlim(xmin=0, xmax=100)
        plt.ylim(ymin=0, ymax=100)
        x = [i.x for i in self.indiv_nodes_as_list]
        y = [i.y for i in self.indiv_nodes_as_list]
        if show_nodes is True:
            plt.scatter(x, y)
        plt.plot(x, y, color=color, zorder=zorder, linewidth=edge_width)

    # def relative_angle(self, other):
    #     # test the angle of self relative to other
    #     avg_node_angle = arctan2()
    #     pass

    # def angle_from(self, zero_angle):
    #     """Returns the directed angle from the defined zero-angle."""
    #     pass


class Path(Sequence):
    """Represents a path as being made of a series of nodes.
    A Path must be given a series (list, tuple) of nodes as the 'path' arg, in the correct order.
    A path is inherently immutable from the perspective of this library.
    The 'nodes' property can be used for mutability purposes."""

    def __init__(self, path=None):
        self.path = tuple(path)

    def __getitem__(self, item):
        return self.path[item]

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return f"{self.path}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        """Paths are treated as being circular, so, in terms of equality, all rotations of a path are considered equal.
        The implementation of this accounts for both paths that are implicitly circular, e.g. ('A', 'B', 'C'), or for
        paths that are explicitly circular, e.g. ('A', 'B', 'C', 'A').
        Currently it will return True if comparing an implicit path to an explicit path.
        """
        if self.path[0] == self.path[-1]:
            path1 = self.path[0:-1]
        else:
            path1 = self.path

        if other.path[0] == other.path[-1]:
            path2 = other.path[0:-1]
        else:
            path2 = other.path

        first_node = path1[0]
        match = 0
        for i, v in enumerate(path2):
            if v == first_node:
                match = i
                break

        path1_index = 0
        path2_index = match
        for i in range(len(path1)):
            path1_node = path1[path1_index]
            path2_node = path2[path2_index]
            if path1_node != path2_node:
                return False

            path1_index += 1
            path2_index = (path2_index + 1) % len(path1)
        return True

    @property
    def nodes(self):
        """Use this property if you want to have a mutable list of the nodes."""
        return list(self.path)

    @property
    def edges(self):
        """Returns the path as a series of edges, preserving the order/direction of the path."""
        edge_path = []
        for index, node in enumerate(self.path):
            if index == len(self.path) - 1:
                break
            next_node = index + 1
            edge = Edge(node, self.path[next_node])
            edge_path.append(edge)
        return edge_path

    @property
    def length(self):
        """Returns the total length of the path."""
        total_length = 0
        if self.path is not None:
            for index, node in enumerate(self.path):
                if index == (len(self.path) - 1):
                    break
                next_node = index + 1
                edge_length = Instance.edge_length(node, self.path[next_node])
                total_length += edge_length
            return total_length
        else:
            raise ValueError("Path was empty.")

    @property
    def average_edge_length(self):
        """Returns the average edge length of the path."""
        return numpy.mean([n.length_ for n in self.edges])

    def n_sorted_edges(self, n, reverse=False):
        """Returns n sorted edges in order, the default being shortest first.
        Change the 'reverse' argument for longest first.
        Multiple edges will be returned if they have the same length."""
        lis = sorted([n for n in self.edges], reverse=reverse)
        if n == 1:
            if lis[0].length_ != lis[1].length_:
                return lis[0]
            else:
                return lis[0].length_, "There is more than one shortest edge."

        elif 1 < n < len(self.nodes):
            return lis[0:n]

        elif n >= len(self.nodes):
            return lis[0:len(self.nodes)], "There are less nodes in total than the given number."

    @property
    def edge_lengths_as_list(self):
        """Returns the edge lengths as a list."""
        return sorted([n.length_ for n in self.edges], reverse=False)

    @property
    def average_node(self):
        """Returns the average node of the path."""
        # 'Set' is used to remove any duplicate nodes, i.e. the last node ususally.
        x_mean = numpy.mean(list(set([node.x for node in self.path])))
        y_mean = numpy.mean(list(set([node.y for node in self.path])))
        return Node(x_mean, y_mean)

    # def view(self, show_avg=False, no_path=False, plot_se=False, plot_le=False, title='', node_color='red',
    #          edge_color='red', edge_zorder=2, node_zorder=3,  edge_width=1):
    #     """Uses matplotlib.pyplot to view the path.
    #     Set show_avg=True to plot the average node. Set no_path=True to plot the nodes only, with no path.
    #     Set plot_se=True and plot_le=True to plot the shortest and longest edges, respectively.
    #     When using this method in a loop, be sure to include a call to 'plt.figure()' in each loop, otherwise all loop
    #     results will be plotted on the same graph.
    #     """
    #     plt.title = title
    #     plt.xlim(xmin=0, xmax=100)
    #     plt.ylim(ymin=0, ymax=100)
    #     if show_avg:
    #         plt.scatter(self.average_node.x, self.average_node.y)
    #     if no_path is True:
    #         plt.scatter([i.x for i in self.path], [i.y for i in self.path])
    #     else:
    #         plt.plot([i.x for i in self.path], [i.y for i in self.path], zorder=edge_zorder, linewidth=edge_width,
    #                  color=edge_color)
    #         plt.scatter([i.x for i in self.path], [i.y for i in self.path], color=node_color, zorder=node_zorder)
    #     if plot_se is True:
    #         plt.plot([i.x for i in self.shortest_edge.indiv_nodes_as_list],
    #                  [i.y for i in self.shortest_edge.indiv_nodes_as_list])
    #     if plot_le is True:
    #         plt.plot([i.x for i in self.longest_edge.indiv_nodes_as_list],
    #                  [i.y for i in self.longest_edge.indiv_nodes_as_list])
    #     plt.show()


class Instance:

    Count = 0

    def __init__(self, seed=None, nodes=None, edges=None, dmatrix=None, solution_path=None, solve_time=None,
                 results=None, relative_edges=False):
        """Create a new problem with x number of nodes.
        Leave seed blank for random seed, otherwise put an eight digit number to use for the seed."""
        self.seed = seed
        self.nodes = nodes
        self.edges = edges
        self.dmatrix = dmatrix
        self.solution_path = solution_path
        self.solve_time = solve_time
        self.results = results
        self.relative_edges = relative_edges
        Instance.Count += 1

    def __str__(self):
        return f"Seed: {self.seed}\n" \
               f"Node count: {self.num_nodes}\n" \
               f"Edge count: {self.num_edges}\n" \
               f"Nodes: {self.nodes}\n" \
               f"Edges: {self.edges}\n" \
               f"Distance matrix: {self.dmatrix}\n" \
               f"Solve time: {self.solve_time}\n" \
               f"Results: {self.results}"

    def __repr__(self):
        return str(self)

    @staticmethod
    def seeder(manual_seed=False, num=None):
        """Leave parameters blank for a random seed, otherwise set manual_seed=True and num=(the seed you want to use).
        Below is an example of it's usage. It should be set before populating the 'nodes' dictionary. A call to
        'Generate.instance(args)' uses this method in the generation process.

        s = Instance.seeder(args)
        instance = Instance()
        instance.seed = s
        instance.populate_nodes()
        """
        if manual_seed is False:
            z = numpy.random.randint(10000000, 99999999)
            numpy.random.seed(z)
            return z
        elif manual_seed is True:
            numpy.random.seed(num)
            return num

    @staticmethod
    def pairs_range(n, r=2):
        """Takes a number 'n' and returns the number of unique pairs from n. Used in populating an instance's edge
        dictionary. The 'r' parameter can be changed if desired, to return sets of a different size."""
        return int((math.factorial(n)) / ((math.factorial(r)) * (math.factorial(n - r))))

    @staticmethod
    def perms_range(n, r=1):
        """Returns the full range of permutations for the instance's edges. This is used by the solve method to exhaust
        the permutations generator without going over the maximum number of permutations."""
        return int((math.factorial(n)) / (math.factorial(n - r)))

    @staticmethod
    def combs_range(n, r=1):
        """Calculates number of combinations."""
        return int((math.factorial(n)) / (math.factorial(r) * math.factorial(n - r)))

    @staticmethod
    def edge(node_one, node_two):
        """Takes two nodes as args and returns an Edge object with those nodes."""
        return Edge(node_one, node_two)

    @staticmethod
    def edge_length(node_one, node_two):
        """Takes two nodes as args and returns the length of the edge in between them."""
        return math.hypot((node_one.x - node_two.x), (node_one.y - node_two.y))

    # @staticmethod
    # def edge_angle(edge):  # TODO: not working currently, need to fix or deprecate
    #     x = arctan2([x1, x2], [y1, y2])
    #     return x

# TODO: write an 'edge-ranks' property, returning a dictionary of nodes, and their respective edges ranked by angle

    @property
    def num_nodes(self):
        """Returns the number of nodes in the 'nodes' dict. This is mainly for the default object print function, as the
        'nodes' dict default value is None which raises an error when trying to print the len... this is a work-around
        that returns the string 'None' instead of the actual value."""
        if self.nodes is not None:
            return len(self.nodes)
        else:
            return "None"

    @property
    def num_edges(self):
        """Returns the number of edges in the 'edges' dict. This is mainly for the default object print function, as the
        'edges' dict default value is None which raises an error when trying to print the len... this is a work-around
        that returns the string 'None' instead of the actual value."""
        if self.edges is not None:
            return len(self.edges)
        else:
            return "None"

    @property
    def x_values(self):
        """Returns the x-coordinate values as a list."""
        x_list = []
        path = [v for k, v in self.nodes.items()]
        for index, node in enumerate(path):
            x_list.append(node.x)
        return x_list

    @property
    def y_values(self):
        """Returns the y-coordinate values as a list."""
        y_list = []
        path = [v for k, v in self.nodes.items()]
        for index, node in enumerate(path):
            y_list.append(node.y)
        return y_list

    @property
    def average_node(self):
        """Calculates the average node and returns a Node object. (Uses the [x/y]_values methods)"""
        x = numpy.mean(self.x_values)
        y = numpy.mean(self.y_values)
        return Node(x, y)

    @property
    def instance_edge_sum(self):  # TODO: test this for correct output
        """Returns the sum of all the edges."""
        return sum(length for length in self.n_edge_lengths(all_lengths=True))

    @property
    def instance_average_edge_length(self):
        """Returns the average edge length for the instance."""
        return numpy.mean([n.length_ for n in self.edges.values()])

    @property
    def nodes_as_plain_data(self):  # TODO: test this for correct output
        """Returns a list of the nodes, but as plain numbers in tuples, not Node objects."""
        nodes = []
        for i in list(self.nodes.values()):
            node = (i.x, i.y)
            nodes.append(node)
        return nodes

    def n_edge_lengths(self, n=None, reverse=False, all_lengths=False):  # TODO: test this for correct output
        """Returns n edge lengths as a list.
        Default is shortest lengths first. Set reverse=True for longest first.
        If all=True, all the edge will be returned, ignoring n."""
        if self.relative_edges:
            step = 2
        else:
            step = 1

        if all_lengths:
            return sorted([n.length_ for n in self.edges.values()], reverse=reverse)
        else:
            return sorted([n.length_ for n in self.edges.values()], reverse=reverse) \
                       [0:len(self.edges.values()):step][0:n]


    # @property
    # def skew_value(self):
    #     """Returns the skew value of the problem.
    #     Empty at the moment, I need to remember how to calculate the skew value.
    #     """

    @property
    def density_dict(self):
        """Returns a dictionary of the node densities."""
        return {key: node.density for key, node in self.nodes.items()}

    def edges_from_node(self, node, good_only=False):
        """Pass in a digit specifying the node to return the connected edges for.
        Will only work if the edges are relative.
        Set good_only=True and only edges with fitness='good' will be returned."""
        n = self.nodes[node]
        if good_only is True:
            return {k: v for (k, v) in self.edges.items() if v.node_one == n and v.fitness == 'good'}
        else:
            return {k: v for (k, v) in self.edges.items() if v.node_one == n}

    def n_nodes_by_dist_to_avg(self, n, reverse=False):  # TODO: test this for correct output
        """Returns a list of n nodes that are closest to the average node."""
        if n > len(self.nodes):
            print('N is more than the number of nodes, so all nodes will be returned in ascending order of distance.')
        return sorted(self.nodes.values(), key=lambda x: x.dist_from_other(self.average_node), reverse=reverse)[0:n]

    def nodes_by_coord_value(self, reverse=False, coord=None):
        """Returns a list of the nodes sorted by either x or y co-ordinates.
        The 'coord' arg must be a string equal to either 'x' or 'y'.
        Default is lowest values first, set reverse=True for longest first."""
        if coord == 'x':
            return sorted(self.nodes.values(), key=lambda x: x.x, reverse=reverse)
        elif coord == 'y':
            return sorted(self.nodes.values(), key=lambda x: x.y, reverse=reverse)

    def n_edges_by_length(self, n, reverse=False):  # TODO: test this for correct output
        """Returns the n shortest edges. Be careful with this method, as there may be more than one edge sharing the
        same length, however this is unlikely in random instances."""
        sorted_edges = sorted(self.edges.values(), key=lambda x: x.length_, reverse=reverse)
        if n == 1:
            return sorted_edges[0]
        elif 1 < n < len(self.nodes):
            return sorted_edges[0:n]
        elif n == len(self.nodes):
            return sorted_edges[0:len(self.nodes)]
        elif n > len(self.nodes):
            print('N is more than the number of edges, so all edges will be returned in order of ascending length.')
            return sorted_edges[0:len(self.nodes)]

    def populate_nodes(self, n):
        """Populates the 'nodes' dictionary with a number of random nodes, based on 'n'."""
        if self.nodes is None:
            self.nodes = {}
            for i in range(n):
                self.nodes[i+1] = Node.random_node()
        else:
            print("The instance's nodes have already been populated.")

    def populate_edges(self, relative_edges=False):
        """Populates the 'edges' dictionary based on the 'nodes' dictionary. Setting relative_edges=True will treat
        edges as relative to the nodes, and not as unique objects, and will generate all possible edges. Leaving
        relative_edges=False will only generate unique/non-mirroring edges."""
        if self.edges is None:
            self.edges = {}
        if relative_edges is False:
            unique_pairs = itertools.combinations(self.nodes.values(), 2)
            for j in range(Instance.pairs_range(len(self.nodes))):
                index = j
                pair = next(unique_pairs)
                self.edges[index+1] = Edge(pair[0], pair[1])
        elif relative_edges is True:
            index = 1
            for n in self.nodes.values():
                for m in self.nodes.values():
                    if n != m:
                        self.edges[index] = Edge(n, m)
                        index += 1

    def populate_dmatrix(self):
        self.dmatrix = []
        for n in self.nodes.values():
            d_list = []
            for m in self.nodes.values():
                d_list.append(n.dist_from_other(m))
            self.dmatrix.append(d_list)

    def solve(self, convex_hull=True, brute_force=True):
        """Solves the instance, if possible, in the quickest way available to this library.
        Solving can also be done manually through calling 'Solver.brute_force(instance)', however this is a more
        direct way to do it."""
        if convex_hull is True:
            self.convex_hull()

        if brute_force is True:
            bf_result = Solver.brute_force(self)

            if self.results is None:
                self.results = {'brute_force': bf_result['path']}

            else:
                self.results['brute_force'] = bf_result['path']

            self.results['optimal_solution'] = self.results['brute_force']
            self.solution_path = bf_result['path']

            return 'Brute force completed.'

        else:
            return 'All arguments were false, no solution found.'

    def convex_hull(self):
        """Solves the convex hull and populates results dict with 'convex_hull' entry."""
        ch_result = Solver.grahams_scan_convex_hull(self)
        if self.results is None:
            self.results = {'convex_hull': ch_result['path']}
            return 'Convex hull found.'
        else:
            self.results['convex_hull'] = ch_result['path']
            return 'Convex hull found.'

    def prune(self):
        """Completes a diamond prune on the instance's edges."""
        reducers.diamond_prune(self)

    # def view(self, result=None, nodes=False, edges=False, show_avg=False, plot_se=False, plot_le=False, title='default',
    #          node_color='red', edge_color='blue', node_zorder=2, edge_zorder=1, edge_width=1, labels=True,
    #          good_edges=False, e_from_single_node=False, node=None):
    #     """Use pyplot to view the instance. It will show the path if the instance has been solved.
    #     Set show_avg=True to plot the average node. Set no_path=True to plot the nodes only, if the instance has been
    #     solved but you don't want to see the path.
    #     Make sure to include 'plt.figure()' in any looping algorithms. This ensures that diferent loops are plotted on
    #     different graphs.
    #     """
    #     if title == 'default':
    #         plt.title = f"Problem: {self.seed}"
    #     else:
    #         plt.title = title
    #
    #     plt.xlim(xmin=0, xmax=100)
    #     plt.ylim(ymin=0, ymax=100)
    #
    #     if result:  # plot the passed result path
    #         self.results[result].view(node_color=node_color, node_zorder=node_zorder, edge_zorder=edge_zorder)
    #
    #     if nodes is True:  # plot the nodes
    #         plt.scatter(self.x_values, self.y_values, color=node_color, zorder=node_zorder)
    #
    #     # if labels is True:  # annotate each node with a label of id and co-ords, not working yet
    #     #     for i in self.nodes.values():
    #     #         plt.annotate()
    #
    #     if edges is True:  # plot all of the instance's edges
    #         for edge in self.edges.values():
    #             edge.plot(color=edge_color, zorder=edge_zorder, edge_width=edge_width)
    #
    #     if good_edges is True:  # plot only the instance's good edges after pruning
    #         for edge in self.edges.values():
    #             if edge.fitness == 'good':
    #                 edge.plot(zorder=edge_zorder, edge_width=edge_width)
    #
    #     if e_from_single_node is True:  # plot the edges from a single node only
    #         for edge in self.edges.values():
    #             if edge.node_one == self.nodes[node]:
    #                 edge.plot(zorder=edge_zorder, edge_width=edge_width)
    #
    #     if show_avg:  # plot the average node
    #         plt.scatter(self.average_node.x, self.average_node.y)
    #
    #     if plot_se is True:  # plot the shortest edge
    #         plt.plot([i.x for i in self.n_shortest_edges_of_instance(1).indiv_nodes_as_list],
    #                  [i.y for i in self.n_shortest_edges_of_instance(1).indiv_nodes_as_list])
    #
    #     if plot_le is True:  # plot the longest edge
    #         plt.plot([i.x for i in self.n_longest_edges_of_instance(1).indiv_nodes_as_list],
    #                  [i.y for i in self.n_longest_edges_of_instance(1).indiv_nodes_as_list])
    #
    #     plt.show()
    #
    # def populate_node_densities(self):
    #     """Sets the node density values."""
    #     inst_edge_sum = self.instance_edge_sum
    #     for node in self.nodes.values():
    #         if node.density is None:
    #             connected_edge_length_sum = 0
    #             for edge in self.edges.values():
    #                 if edge.node_one == node or edge.node_two == node:
    #                     connected_edge_length_sum += edge.length_
    #             node.density = connected_edge_length_sum/inst_edge_sum


class Generator:

    @staticmethod
    def new_instance(node_count=None, empty=False, source='random', file=None, seed='random', solve=False,
                     relative_edges=True, calc_node_densities=False, calc_dmatrix=False):
        # TODO: change implementation of sources to use arg 'data' rather than multiple args of different types
        """This method will return an instance, with some options for the result.
        Setting 'empty' to True will return an unpopulated instance. This is handy when you want to populate the nodes
        from your own data sets.
        Nodes are generated from a random seed. Setting seed equal to any number will generate a seed equal to that
        number, from which the nodes will be populated. Thus, any previously generated problem can be re-created for
        further testing by setting seed equal to the desired number. Random seeds are eight digits long.
        The solve parameter is self-descriptive.
        Setting rel_edges=False will treat edges as unique, thus an instance with three nodes will have the three unique
        edges generated instead of the six relative edges.
        Setting calc_node_dens=True will populate the node densities. This calculation measures the position of a node,
        relative to the other nodes.
        Setting calc_dmatrix=True will calculate the distance matrix and set the dmatrix attribute accordingly."""

        def random_source():
            """Generates a random eight digit seed for generating random nodes."""
            if node_count < 3:
                print('The node_count given is less than three and is invalid. This value must be three or greater.')
                raise ValueError
            s = Instance.seeder()
            inst = Instance(relative_edges=relative_edges)
            inst.seed = s
            inst.populate_nodes(node_count)
            inst.populate_edges(relative_edges=relative_edges)
            return inst

        def seed_source():
            """Generate an instance from a given integer as a seed. This allows reproducibility in terms of the seed
            used.
            random_source will also generate a seed, but the seed is random and not known until after generation. This
            can be recorded and stored for the purpose of reproducibility in the same way."""
            if node_count < 3:
                print('The node_count given is less than three and is invalid. This value must be three or greater.')
                raise ValueError
            s = Instance.seeder(manual_seed=True, num=seed)
            inst = Instance(relative_edges=relative_edges)
            inst.seed = s
            inst.populate_nodes(node_count)
            inst.populate_edges(relative_edges=relative_edges)
            return inst

        def csv_source():  # TODO: add check to make sure file is .csv format
            """Generates an instance from a csv of x/y values.
            Argument must include the full file-path plus the full filename including '.csv'.
            Setting rel_edges=False will treat edges as unique, thus an instance with three nodes will have the three
            unique edges generated instead of the six relative edges.
            Setting calc_dmatrix=True will calculate the distance matrix and set the dmatrix attribute accordingly.
            Setting calc_node_dens=True will populate the node densities. This calculation determines the position of a
            node, relative to the other nodes."""
            inst = Instance(relative_edges=relative_edges)
            if inst.nodes is None:
                inst.nodes = {}
            with open(file) as data:
                reader = csv.DictReader(data)
                for index, row in enumerate(reader):
                    inst.nodes[index + 1] = Node(row['x'], row['y'])
            inst.populate_edges(relative_edges=relative_edges)
            return inst

        # def jpg_source():  # TODO: add check to make sure file is .jpg format
        #     inst = Generator.new_instance(empty=True)
        #     image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        #     image = cv2.flip(image, 0)
        #     params = cv2.SimpleBlobDetector_Params()
        #     params.minThreshold = 10
        #     params.maxThreshold = 200
        #     params.filterByArea = True
        #     params.minArea = 1
        #     detector = cv2.SimpleBlobDetector_create(params)
        #     keypoints = detector.detect(image)
        #     inst.node_count = len(keypoints)
        #     if inst.nodes is None:
        #         inst.nodes = {}
        #     index = 0
        #     for point in keypoints:
        #         point = Node(int(point.pt[0]), int(point.pt[1]))
        #         inst.nodes[index] = point
        #         index += 1
        #     inst.populate_edges(relative_edges=relative_edges)
        #     return inst

        # def list_source():
        #     inst = Instance()

        # def tsplib_source():

        if empty is True:
            return Instance()
        elif source == 'random':
            instance = random_source()
        elif source == 'seed':
            instance = seed_source()
        elif source == 'csv':
            instance = csv_source()
        # elif source == 'jpg':  # to be added in the future
        #     instance = jpg_source()
        # elif source == 'pylist':  # to be added in the future
        #     instance = list_source()
        # elif source == 'tsp-lib':  # to be added in the future
        #     pass

        if calc_node_densities is True:
            instance.populate_node_densities()

        if calc_dmatrix is True:
            instance.populate_dmatrix()

        if solve is True:  # TODO: add check for amount of nodes, raise warning if too many
            instance.solve()

        return instance


class Solver:

    @staticmethod
    def brute_force(instance):
        """Calculates the optimal solution and length using brute force on loops only beginning and
        ending with a particular element.
        Leaving return_only=True means that this method will only return the shortest path. Otherwise, setting it to
        True will make this function automatically try to populate the results dictionary for the instance it was called
        on. This is helpful when carrying out a simple brute force on an instance."""
        # check argument size for greater than 3
        if len(instance.nodes) > 3:

            # check argument size for greater than 11
            if len(instance.nodes) > 11:
                print()
                ans = input("11 nodes takes 180 seconds, more than that will take a few hours.\n"
                            "Would you like to continue? (y/n) ")
                if ans != "y":
                    return

            start = time.time()

            # store the last node to a variable, this will be used to complete the loops
            last_elem = instance.nodes[len(instance.nodes)]

            # remove the last node to permute on the rest of the nodes only
            instance.nodes.pop(len(instance.nodes))

            # calculate the permutation range, which will be used to empty the generator
            perm_range = Instance.perms_range(len(instance.nodes), r=len(instance.nodes))

            # create the permutations generator
            permutations = itertools.permutations(instance.nodes.values())

            # set the path length equal to infinity so that the first calculated path is guaranteed to be less
            shortest_path_length = float("inf")
            shortest_path = ()  # this means that Path will be a tuple...

            for i in range(perm_range):  # exhaust the generator without throwing an error
                permutation = next(permutations)

                permutation = (last_elem,) + permutation + (last_elem,)  # appending the first element to start/end

                total_length = 0  # initialise temporary length variable, reset at each loop

                for index, node in enumerate(permutation):  # need enumerate for the index
                    if index == len(instance.nodes) + 1:  # break before trying to do edge operation on the last node
                        break
                    next_node = index + 1
                    edge = Instance.edge_length(node, permutation[next_node])
                    total_length += edge
                    if total_length > shortest_path_length:
                        break
                if total_length <= shortest_path_length:
                    shortest_path_length = total_length
                    shortest_path = Path(tuple(permutation))

            end = time.time()
            instance.solve_time = end - start

            instance.nodes[len(instance.nodes) + 1] = last_elem
            # instance.solution_path = shortest_path

            return {'path': shortest_path}

        elif len(instance.nodes) == 3:
            return {'path': Path(path=[instance.nodes[1], instance.nodes[2], instance.nodes[2]])}
        elif len(instance.nodes) < 3:
            return "There were less than three nodes given. Three or more nodes must be given."

    @staticmethod
    def grahams_scan_convex_hull(instance):
        from functools import reduce
        """
        Returns points on convex hull in CCW order according to Graham's scan algorithm.
        Credit to Tom Switzer <thomas.switzer@gmail.com>.
        Found at https://gist.github.com/arthur-e/5cf52962341310f438e96c1f3c3398b8
        I've edited so that it returns a Path object in the instance's results dict.
        """
        points = instance.nodes_as_plain_data
        turn_left, turn_right, turn_none = (1, -1, 0)

        def cmp(a, b):
            return (a > b) - (a < b)

        def turn(p, q, r):
            return cmp((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]), 0)

        def _keep_left(hull, r):
            while len(hull) > 1 and turn(hull[-2], hull[-1], r) != turn_left:
                hull.pop()
            if not len(hull) or hull[-1] != r:
                hull.append(r)
            return hull

        points = sorted(points)
        l = reduce(_keep_left, points, [])
        u = reduce(_keep_left, reversed(points), [])
        res = l.extend(u[i] for i in range(1, len(u) - 1)) or l  # the original algorithm's return value

        # create a Path and populate the results dict
        path = []
        for i in res:
            path.append(Node(i[0], i[1]))
        path.append(path[0])

        return {'path': Path(tuple(path))}

# path view(self, show_avg=False, no_path=False, plot_se=False, plot_le=False, title='', node_color='red',
#           edge_color='red', edge_zorder=2, node_zorder=3,  edge_width=1)

# instance view(self, result=None, nodes=False, edges=False, show_avg=False, plot_se=False, plot_le=False,
#               title='default', node_color='red', edge_color='blue', node_zorder=2, edge_zorder=1, edge_width=1,
#               labels=True, good_edges_only=False, e_from_single_node=False, node=None)

# Both a Path and an Instance have 'nodes' and 'edges' properties, so both can be accessed with the same call.
# I should be able to use that fact to make that code simpler.

# plot all nodes > red
# plot edges
# if good_edges_only:
#     only plot good edges
# else:
#     plot all edges
# plot single edge if given (overrides plotted edge above with different colour)

# TODO: implement labels for nodes


def view(data, nodes=False, edges=False, good_edges_only=False, show_avg=False, plot_se=False, plot_le=False,
         node_color='red', edge_color='blue', node_zorder=2, edge_zorder=1, edge_width=1, e_from_single_node=False,
         node=None):
    """An Instance or a Path needs to be given as the 'data' arg.
    Plots nodes, edges and paths; can also plot the average node, any single edge"""
    plt.xlim(xmin=0, xmax=100)
    plt.ylim(ymin=0, ymax=100)

    if nodes:  # plot the nodes
        plt.scatter(data.x_values, data.y_values, color=node_color, zorder=node_zorder, )

    if edges:  # plot all of the instance's edges
        if good_edges_only:
            for edge in data.edges.values():
                if edge.fitness == 'good':
                    edge.plot(zorder=edge_zorder, edge_width=edge_width)
        else:
            for edge in data.edges.values():
                edge.plot(color=edge_color, zorder=edge_zorder, edge_width=edge_width)

    if e_from_single_node:  # plot the edges from a single node only
        try:
            for edge in data.edges.values():
                if edge.node_one == data.nodes[node]:
                    edge.plot(zorder=edge_zorder, edge_width=edge_width, edge_color='green')
        except Exception as e:
            print(e)

    if show_avg:  # plot the average node
        plt.scatter(data.average_node.x, data.average_node.y, marker=data.average_node.nodes)

    if plot_se is True:  # plot the shortest edge
        plt.plot([i.x for i in data.n_shortest_edges_of_instance(1).indiv_nodes_as_list],
                 [i.y for i in data.n_shortest_edges_of_instance(1).indiv_nodes_as_list])

    if plot_le is True:  # plot the longest edge
        plt.plot([i.x for i in data.n_longest_edges_of_instance(1).indiv_nodes_as_list],
                 [i.y for i in data.n_longest_edges_of_instance(1).indiv_nodes_as_list])

    plt.show()
