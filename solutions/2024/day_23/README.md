# Day 23 (2024)

`LAN Party` ([prompt](https://adventofcode.com/2024/day/23))

Today's problem was about graphs and identifying cycles, which can be done easily (but slowly) using the `networkx` module or with a faster approach.

# Solution using `networkx`
With this module, we can simply create a `Graph` object and add the edges given to us in the input. To find cycles of length 3 we simply use the `simple_cycles` function and return the result.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        g = networkx.Graph()
        g.add_edges_from(line.rstrip().split("-") for line in self.input)
        return sum(
            any(str(node).startswith("t") for node in cycle)
            for cycle in networkx.simple_cycles(g, length_bound=3)
        )
```
Similarly for Part 2, we just need to find the largest fully connected subnet which can be easily done with `aproximation.max_clique`. This approach is very simple to code but it has a pretty slow execution time of over a minute for both parts which is definitely too long for my AoC objectives.
```py
class Solution(StrSplitSolution):
    def part_2(self) -> str:
        g = networkx.Graph()
        g.add_edges_from(line.rstrip().split("-") for line in self.input)
        largest_subnet = networkx.approximation.max_clique(g)
        return ",".join(sorted(largest_subnet))
```
## Part 1
In this case, I prefered to represent the graph with a `dict` that will hold an adjacency list for each node. In the following code snippet you can see how this is created.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        edges = [line.strip().split("-") for line in self.input]
        G = {}
        for edge in edges:
            if edge[0] not in G:
                G[edge[0]] = []
            G[edge[0]].append(edge[1])
            if edge[1] not in G:
                G[edge[1]] = []
            G[edge[1]].append(edge[0])
```
For this first part, as I said before, the objective is to count cycles of length 3 that additionally one of the nodes starts with the letter `t`. To do this, for each `vertex` or node, we try to find two neighbors that are connected to each other which would give us a cycle, and after adding it to a `set` to avoid duplicates we increase the count if it meets the second condition.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        ...
        result = 0
        for vertex, neighbors in G.items():
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in G[neighbors[i]]:
                        s = sorted([vertex, neighbors[i], neighbors[j]])
                        if tuple(s) not in connected_sets_of_3:
                            result += 1 if any(x[0] == "t" for x in s) else 0
                        connected_sets_of_3.add(tuple(s))
        return result
```

## Part 2
In this second part, the objective is to identify the largest fully connected subnet in the graph, and return the nodes of the largest subnet as a comma-separated string in order.

To do this, first we need a helper function that given a list of nodes will tell us if they form a fully connected subnet.
```py
def all_connected(nodes: tuple, g: dict) -> bool:
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in g[nodes[i]]:
                return False
    return True
```
The final solution:
1. Iterates over all neighbors of a vertex.
2. Uses `itertools.combinations` to test subsets of neighbors for full connectivity using the all_connected helper function.
3. Updates the largest clique if a larger fully connected subset is found.
```py
class Solution(StrSplitSolution):
    def part_2(self) -> str:
        ...

        best_connected_set = []
        for vertex, neighbors in G.items():
            for i in range(len(neighbors), 1, -1):
                if i < len(best_connected_set):
                    break
                for comb in itertools.combinations(neighbors, r=i):
                    if all_connected(comb, G):
                        best_connected_set = max(
                            list(comb) + [vertex], best_connected_set, key=len
                        )
                        break
        best_connected_set.sort()
        return ",".join(map(str, best_connected_set))
```
