import unittest
from opentsp.objects import Node
from opentsp.objects import Edge
from opentsp.objects import Generator


class NodeTestCase(unittest.TestCase):

    def setUp(self):
        self.node = Node()
        self.populatednode = Node(2, 3)

    def tearDown(self):
        print('Tear-down success.')

    def test_Node(self):
        self.assertEqual(self.node.x, 0, 'Default node x value failed.')
        self.assertEqual(self.node.y, 0, 'Default node y value failed.')

        self.node.x = 2
        self.node.y = 3

        self.assertEqual(self.node.x, 2, 'Node x value change failed.')
        self.assertEqual(self.node.y, 3, 'Node y value change failed.')


class EdgeTestCase(unittest.TestCase):

    def setUp(self):
        edge_node_one = Node(2, 3)
        edge_node_two = Node(6, 7)
        self.edge = Edge(edge_node_one, edge_node_two)
        self.midpoint_node = Node(4, 5)

    def tearDown(self):
        print('Tear-down success.')

    def test_Edge(self):
        self.assertEqual(self.edge.length_, 5.656854249492381)
        self.assertEqual(self.edge.midpoint, self.midpoint_node)


# TODO: implement tests on the Path class


class InstanceTestCase(unittest.TestCase):

    def setUp(self):
        node_one = Node(51, 98)
        node_two = Node(31, 4)
        node_three = Node(49, 80)
        node_four = Node(43, 47)
        edge_one = Edge(node_one, node_two)
        edge_two = Edge(node_one, node_three)
        edge_three = Edge(node_one, node_four)
        edge_four = Edge(node_two, node_three)
        edge_five = Edge(node_two, node_four)
        edge_six = Edge(node_three, node_four)
        self.prob = Generator.new_instance(node_count=4, source='seed', seed=12345678, solve=True, relative_edges=False)
        self.compare_nodes_dict = {1: node_one, 2: node_two, 3: node_three, 4: node_four}
        self.compare_edges_dict = {1: edge_one, 2: edge_two, 3: edge_three, 4: edge_four, 5: edge_five, 6: edge_six}

    def tearDown(self):
        print('Tear-down success')

    def test_Instance(self):
        self.assertEqual(self.prob.nodes, self.compare_nodes_dict)
        self.assertEqual(self.prob.edges, self.compare_edges_dict)
        self.assertEqual(self.prob.seed, 12345678)
        self.assertEqual(self.prob.edge_length(self.prob.nodes[1], self.prob.nodes[2]), 96.1041102138717)
        self.assertEqual(self.prob.x_values[0], 51)
        self.assertEqual(self.prob.y_values[0], 98)
        self.assertEqual(self.prob.average_node, Node(43.5, 57.25))
        self.assertEqual(self.prob.instance_edge_sum, 322.12506347937057)
        self.assertEqual(self.prob.results['optimal_solution'].length, 192.3989287237428)
        self.assertEqual(self.prob.instance_average_edge_length, 53.6875105798951)
        self.assertEqual(self.prob.n_closest_nodes_to_avg_node(2), [Node(43, 47), Node(49, 80)])
        self.assertEqual(self.prob.n_farthest_nodes_from_avg_node(2), [Node(31, 4), Node(51, 98)])
        self.assertEqual(self.prob.nodes_by_x_value()[0], Node(31, 4))
        self.assertEqual(self.prob.nodes_by_y_value()[0], Node(31, 4))
        self.assertEqual(self.prob.n_shortest_edges_of_instance(1).length_, min(self.prob.edge_lengths_as_list))
        self.assertEqual(self.prob.n_longest_edges_of_instance(1).length_, max(self.prob.edge_lengths_as_list))


if __name__ == '__main__':
    unittest.main()
