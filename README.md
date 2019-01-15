# OpenTSP

---
OpenTSP is designed to make it as easy as possible to generate and test TSP instances against hypotheses, as well as solving them with brute force for comparison.  
This is my first major project, having learnt Python over the last six months, so if you have style suggestions I'd love to hear them.

The goal is to make this an easy library to work with, please feel free to email me with any functionality you feel would help.

If you want to contribute implementations of algorithms for solving then I'd love to hear from you! Currently I have implemented *brute-force* and *convex-hull*. However, there is a long list of algorithms I'd love to include in the library, such as *christofides* and *branch and bound*. I don't have the knowledge to implement these myself though.  
This is why I'm making *opentsp* an open-source library, in the hopes that others who find it useful will add to it. If you have suggestions or code, please create a pull request on the Github page, which I'll put the link up for soon.

## Getting started

---
To install *opentsp* in your local environment with pip:
```
pip install opentsp
```
  
Then, at the top of your module:
```
from opentsp.objects import Generator
```



### Creating a TSP Instance

To create a random TSP instance with eight nodes, using your console:
```
>>> from opentsp.objects import Generator
>>> gen = Generator()
>>> instance = gen.new_instance(8)
```

If you want to get the same values as in these examples, then use the below input:
```
>>> instance = gen.new_instance(8, source='seed', seed=1234) 
```

To see what this creates:
```
>>> instance
Seed: 1234
Node count: 8
Edge count: 56
Nodes: {1: (47, 83), 2: (38, 53), 3: (76, 24), 4: (15, 49), 5: (23, 26), 6: (30, 43), 7: (30, 26), 8: (58, 92)}
Edges: {1: ((47, 83), (38, 53), None, False, 0, good, 0), 2: ((47, 83), (76, 24), None, False, 0, good, 0), 3:...}
Distance matrix: None
Solve time: None
Results: None
```

It has a seed, which is used to generate the random nodes. The number of nodes and edges are not object attributes, they come from two class methods, I've found it handy to have that information as part of the printed representation.  
Then it shows the actual nodes and edges, the distance matrix (if generated), the solve time (if brute-forced), and the results.
Results is dictionary of algorithms and their results as a path of nodes.
Something to note here is that edge lengths are only calculated when first needed, and only calculated once. So you can see a 'None' value in the edges, because the lengths haven't been calculated yet. I'll address the Edge class attributes in more detail later.


The instance has a bunch of methods for accessing different properties of a TSP problem, such as: 

- the number of nodes
```
>>> instance.num_nodes
8
```

- number of edges
```
>>> instance.num_edges
56
```

- the *x* and *y* values, for instance:
```
>>> instance.x_values
[47, 38, 76, 15, 23, 30, 30, 58]
```

- the edge lengths:
```
>>> instance.edge_lengths_as_list
[7.0, 7.0, 12.806248474865697, 12.806248474865697, 14.212670...]
```

- the *n* shortest edges:
```
>>> instance.n_shortest_edges_of_instance(1)
((23, 26), (30, 26), 7.0, False, 0, good, 0)
```

- etc

The instance can also be solved, currently the default solve method is brute force.
You can then print the instance's `results` dictionary to look at the results.
```
>>> instance.solve()
'Brute force completed.'
>>> instance.results
{'convex_hull': [(15, 49), (23, 26), (76, 24), (58, 92), (47, 83), (15, 49)], 'brute_force': ((58, 92), (76, 24), (30, 26), (23, 26), (15, 49), (30, 43), (38, 53), (47, 83), (58, 92))}
```

Instances can be generated from a variety of sources, currently these are:  
* **Random**  
   A random eight digit seed is generated for the instance, and nodes with random values are generated from this seed.
* **Seed**  
   Pass in an integer to use as a seed. This is primarily helpful when you want to reproduce a series of random instances. When passing in your own seed make sure to set `source=seed`, otherwise the seed you pass will be ignored.  
   E.g. `inst = generate.Generator.new_instance(5, source='seed', seed=123)`
* **CSV**  
   Currently this takes a CSV with two columns of values for the *x* and *y* coordinates. The top row must have the titles 'x' and 'y'.

Any instance can also be viewed via *matplotlib*, try the two commands below:
```
>>> instance.view(nodes=True, edges=True)
>>> instance.view(result='brute_force')  # must have solved the problem already
```
(The string passed in the result argument above should match a key in the `instance.results` dictionary of the instance. If the problem was solved without need for brute force, then the 'brute_force' key won't be present. However, the 'optimal_solution' key is always present if a solution has been found.)

---
### Example Hypothesis-test Algorithm

Here is an example algorithm, making use of open-tsp's features to generate and test many instances against a hypothesis:
```
import open-tsp as ot

# hypothesis: the shortest edge is always used in the optimal solution

def hyp_test():

    loop = True
    loops = 0
    start = time.time()
    
    while loop is True and loops < 1000000:
        loopstr = f"Failed on loop: {loops}"
        p = ot.classes.Generator.new_instance(6, solve=True)
        shortest_edge = p.n_shortest_edges_of_instance(1)
        edge_path = p.solution_as_edges
        
        if shortest_edge in edge_path:
            loops += 1
            
        else:
            loop = False
            p.view(plot_se=True)
            
    end = time.time()
    total_time = end - start
    print(loopstr)
    print("Took {0}'s to run.".format(total_time))
    print("Finished")
```
This function will generate up to a million instances, testing each one to see if the shortest edge is in the solution or not using the `if` test on line 13: `if shortest_edge in edge_path:`.  
When the test fails, it shows the instance that failed with *matplotlib* and highlights the shortest edge `p.view(plot_se=True)`.  
As you can see, in 19 lines of code it's possible to test a hypothesis, with only a few lines actually concerned with generating the tsp instance and getting it's properties.  
Also, as in the example above, you can solve the instance as part of generating it with `solve=True`. Keep in mind that is most likely going to be a brute force solution, so trying to do this with a 20 node problem will take a fairly long while unless you are running your code on a very powerful supercomputer.

---
### Using Your Own Algorithms

To use your own algorithm, define a function with an appropriate name, and make `instance` an argument.  
```
def brute_force(instance):
```
Write your algorithm within the function.

Then, within the function, you can pass in the instance being worked with and use any of it's attributes or properties.  

For instance, in my brute force algorithm:
```
# store the last node to a variable, this will be used to complete the loops
last_elem = instance.nodes[len(instance.nodes)]
```

To check out the full brute force algorithm, look at the `Solvers` class in the Github repo.

### Overview of Classes

#### Node

Basic point-type class for defining nodes.

I refer to the points in a tsp as 'nodes' rather than 'cities'. Cities is too specific for me, it could just as easily be towns, or cats, really. I prefer the more abstract 'nodes'.

Necessary arguments: *x, y*

#### Edge

Defines the edges as having two nodes and a length. The two nodes inherently bound the length.

Necessary arguments: *node_one, node_two*

#### Path

A path is a series of nodes, and has methods to find the length of the path, etc.

Necessary arguments: *a list of node objects*

#### Instance

Each instance is essentially a container for the nodes, edges and algorithm results.

Necessary arguments: *none*  

This class is not really meant to be created directly as that requires a lot of code, especially for generating the edges, and it would defeat the whole purpose of this library if you had to write all of that. So, the `Generator` class is used to create instances through the `new_instance` method, which contains all of that functionality.

#### Generator

Contains the main method for creating an instance - `new_instance`.

The only required argument for `new_instance` is the number of nodes. In this case, the default is to generate random nodes.

#### Solver

Contains methods for solving instances.


## Update history

1.1.3
  * Added support for indexing/slicing Path objects
  * Path matching now accounts for all rotations of the same path
