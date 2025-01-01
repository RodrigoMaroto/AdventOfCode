# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/23

import itertools

from ...base import StrSplitSolution, answer


def all_connected(nodes: tuple, g: dict) -> bool:
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in g[nodes[i]]:
                return False
    return True


class Solution(StrSplitSolution):
    _year = 2024
    _day = 23

    """
    @answer(1077)
    @slow
    def part_1(self) -> int:
        g = networkx.Graph()
        g.add_edges_from(line.rstrip().split("-") for line in self.input)
        return sum(
            any(str(node).startswith("t") for node in cycle)
            for cycle in networkx.simple_cycles(g, length_bound=3)
        )

    @answer("bc,bf,do,dw,dx,ll,ol,qd,sc,ua,xc,yu,zt")
    @slow
    def part_2(self) -> str:
        g = networkx.Graph()
        g.add_edges_from(line.rstrip().split("-") for line in self.input)
        largest_subnet = networkx.approximation.max_clique(g)
        return ",".join(sorted(largest_subnet))
    """

    @answer(1077)
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
        connected_sets_of_3 = set()
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

    @answer("bc,bf,do,dw,dx,ll,ol,qd,sc,ua,xc,yu,zt")
    def part_2(self) -> str:
        edges = [line.strip().split("-") for line in self.input]
        G = {}
        for edge in edges:
            if edge[0] not in G:
                G[edge[0]] = []
            G[edge[0]].append(edge[1])
            if edge[1] not in G:
                G[edge[1]] = []
            G[edge[1]].append(edge[0])

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

    @answer((1077, "bc,bf,do,dw,dx,ll,ol,qd,sc,ua,xc,yu,zt"))
    def solve(self) -> tuple[int, str]:
        edges = [line.strip().split("-") for line in self.input]
        G = {}
        for edge in edges:
            if edge[0] not in G:
                G[edge[0]] = []
            G[edge[0]].append(edge[1])
            if edge[1] not in G:
                G[edge[1]] = []
            G[edge[1]].append(edge[0])

        connected_sets_of_3 = set()
        part1 = 0
        for vertex, neighbors in G.items():
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in G[neighbors[i]]:
                        s = sorted([vertex, neighbors[i], neighbors[j]])
                        if tuple(s) not in connected_sets_of_3:
                            part1 += 1 if any(x[0] == "t" for x in s) else 0
                        connected_sets_of_3.add(tuple(s))

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
        return part1, ",".join(map(str, best_connected_set))
