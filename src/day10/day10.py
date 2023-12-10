"""
Author: Nat with Darren's Template
Date: 2023-12-10

Solving https://adventofcode.com/2023/day/10

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
from collections import defaultdict

YEAR = 2023
DAY = 10

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

S = ac.Point(0, 1)
N = ac.Point(0, -1)
E = ac.Point(1, 0)
W = ac.Point(-1, 0)

pipes = {
    "-": (E, W),
    "|": (N, S),
    "7": (S, W),
    "F": (S, E),
    "J": (N, W),
    "L": (N, E),
}

opposite = {E: W, W: E, N: S, S: N}


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    maze = {}
    start = None
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c != ".":
                maze[ac.Point(x, y)] = c
            if c == "S":
                start = ac.Point(x, y)
    logger.debug(start)
    # which directions have pipes entering start?
    valid = []
    # check E
    go_east = maze.get(start + E, ".")
    if go_east in pipes and W in pipes[go_east]:
        valid.append(E)
    # check W
    go_west = maze.get(start + W, ".")
    if go_west in pipes and E in pipes[go_west]:
        valid.append(W)
    # check N
    go_north = maze.get(start + N, ".")
    if go_north in pipes and S in pipes[go_north]:
        valid.append(N)
    # check S
    go_south = maze.get(start + S, ".")
    if go_south in pipes and N in pipes[go_south]:
        valid.append(S)
    # decode valid pipes
    valid_pipes = [
        pipe for pipe in pipes if pipes[pipe][0] in valid and pipes[pipe][1] in valid
    ]
    logger.debug(valid_pipes)
    start_pipe = valid_pipes[0]
    maze[start] = start_pipe
    # let's explore!
    count = 0
    current = start
    # pick a direction

    last_direction = pipes[maze[current]][0]
    logger.debug("starting %s", last_direction)
    while True:
        current = current + last_direction
        count += 1
        if current == start:
            break
        if current not in maze:
            logger.error("off map?! %s", current)
            return
        logger.debug("moved %s to %s", last_direction, current)
        exits = [
            exit for exit in pipes[maze[current]] if exit != opposite[last_direction]
        ]
        if len(exits) != 1:
            logger.error("too many exits %s", current)
            return
        last_direction = exits[0]
    logger.info("Part 1: %d", count / 2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
