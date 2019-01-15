import time
from other.generate import Generator


# hypothesis 1: the shortest edge is always used in the solution
def hypothesis_one():
    bool_var = True
    loops = 0
    start = time.time()
    while bool_var is True and loops < 1000000:
        loopstr = f"Failed on loop: {loops}"
        p = Generator.new_instance(6, solve=True)
        shortest_edge = p.n_shortest_edges_of_instance(1)
        edge_path = p.solution_as_edges
        if shortest_edge in edge_path:
            loops += 1
        else:
            bool_var = False
            p.view(plot_se=True)
    end = time.time()
    total_time = end - start
    print(loopstr)
    print("Took {0}'s to run.".format(total_time))
    print("Finished")


# hypothesis 2: the longest edge is never used in instances above a certain number of nodes
def hypothesis_two():
    bool_var = True
    loops = 0
    start = time.time()
    while bool_var is True and loops < 1000000000:
        loopstr = f"Failed on loop: {loops}"
        p = Generator.new_instance(9, solve=True)
        longest_edge = p.n_longest_edges_of_instance(1)
        edge_path = p.solution_as_edges
        if longest_edge not in edge_path:
            loops += 1
            if loops % 100 == 0:
                print(f"Loops: {loops}")
                current = time.time()
                print(f"Time so far is: {current - start}'s")
            pass
        else:
            bool_var = False
            end = time.time()
            total_time = end - start
            print()
            print(loopstr)
            print(f"Took {total_time}'s to run.")
            print("Finished")
            p.view(plot_le=True)

# results for x nodes:
# 4 nodes: not true
# 5 nodes: not true
# 6 nodes: not true, but it takes longer to reach that state
# 7 nodes: not true, same as above, plus more
# 8 nodes: ditto
# 9 nodes:


# hypothesis: the longest edge being in the convex hull and the solution is mutually inclusive, 100% of the time
# False
# hypothesis: if the longest edge is in the solution then it will be in the hull, but that doesn't mean it will be in
# the solution if it is in the hull...
def hypothesis_three():
    var = True
    index = 1
    count = 0
    while var is True:
        p = Generator.new_instance(7, solve=True)
        p.convex_hull()
        hull_as_edges = p.results['convex_hull'].edges
        longest = p.n_longest_edges_of_instance(1)
        if longest in p.solution_path.edges and longest in hull_as_edges:
            print(f'The longest edge was in the solution and the hull on loop {index}.')
            index += 1
        elif longest in p.solution_path.edges and longest not in hull_as_edges:
            print(f'The longest edge was in the solution but not the hull.')
            p.view(result='brute_force')
            var = False
        elif longest not in p.solution_path.edges and longest in hull_as_edges:
            count += 1
            print(f'The longest edge was in the hull but not the solution on loop {index}.'
                  f' This has happened {count} times.')
            index += 1
        elif longest not in p.solution_path.edges and longest not in hull_as_edges:
            index += 1


if __name__ == '__main__':
    hypothesis_three()
