"""
Author: Nat with Darren's Template
Date: 2023-12-25

Solving https://adventofcode.com/2023/day/25

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
import networkx as nx

YEAR = 2023
DAY = 25

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    wires = dict()
    for line in data:
        left, right = line.split(": ")
        right = right.split(" ")
        if left in wires:
            wires[left].extend(right)
        else:
            wires[left] = right
        for node in right:
            if node not in wires:
                wires[node] = [left]
            else:
                wires[node].append(left)
    for wire in wires:
        logger.debug("%s has %d connections", wire, len(wires[wire]))

    # cheat to win!
    graph = nx.Graph()
    for wire in wires:
        graph.add_edges_from((wire, u) for u in wires[wire])

    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    a, b = nx.connected_components(graph)
    result = len(a) * len(b)

    logger.info("Part 1: %s", result)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
