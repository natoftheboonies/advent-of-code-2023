"""
Author: Nat with Darren's Template
Date: 2023-12-16

Solving https://adventofcode.com/2023/day/16

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
from enum import Enum

YEAR = 2023
DAY = 16

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


class Heading(Enum):
    N = (0, -1)
    S = (0, 1)
    E = (1, 0)
    W = (-1, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def turn_left(self):
        return Heading((self.value[1], -self.value[0]))

    def turn_right(self):
        return Heading((-self.value[1], self.value[0]))

    def move(self, x, y, distance=1):
        return (x + self.value[0] * distance, y + self.value[1] * distance, self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def explore(data, start=(0, 0, Heading.E)):
    rows = len(data)
    cols = len(data[0])
    queue = []
    visited = set()
    queue.append(start)
    while queue:
        x, y, heading = queue.pop(0)
        # logger.debug(f"({x},{y}) {heading}")
        if (x, y, heading) in visited or x < 0 or x >= cols or y < 0 or y >= rows:
            continue
        visited.add((x, y, heading))
        if data[y][x] in "\/":
            # logger.debug(f"Found curve {data[y][x]} at ({x},{y})")
            if heading in (Heading.N, Heading.S):
                now_heading = (
                    heading.turn_right() if data[y][x] == "/" else heading.turn_left()
                )
            else:
                now_heading = (
                    heading.turn_left() if data[y][x] == "/" else heading.turn_right()
                )
            queue.append((now_heading.move(x, y)))
        elif data[y][x] == "|" and heading in (Heading.E, Heading.W):
            # logger.debug(f"Splitting {data[y][x]} at ({x},{y})")
            queue.append((Heading.N.move(x, y)))
            queue.append((Heading.S.move(x, y)))
        elif data[y][x] == "-" and heading in (Heading.N, Heading.S):
            # logger.debug(f"Splitting {data[y][x]} at ({x},{y})")
            queue.append((Heading.E.move(x, y)))
            queue.append((Heading.W.move(x, y)))
        else:
            # logger.debug("error %s", data[y][x])
            # assert data[y][x] == "."
            queue.append((heading.move(x, y)))
    # logger.debug(f"Visited: {visited}")

    unique_locations = set()
    for x, y, _ in visited:
        unique_locations.add((x, y))
    return len(unique_locations)


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = [list(data.strip()) for data in f.read().splitlines()]

    logger.info("Part 1: %d", explore(data))

    # Part 2
    max_energy = 0
    for row in range(len(data)):
        # enter left and right
        for heading in (Heading.E, Heading.W):
            x = 0 if heading == Heading.E else len(data[0]) - 1
            energy = explore(data, (x, row, heading))

            if energy > max_energy:
                logger.debug(f"Energy {x},{row},{heading}: {energy}")
                max_energy = energy

    for col in range(len(data[0])):
        # enter top and bottom
        for heading in (Heading.N, Heading.S):
            y = 0 if heading == Heading.S else len(data) - 1
            energy = explore(data, (col, y, heading))

            if energy > max_energy:
                logger.debug(f"Energy {x},{row},{heading}: {energy}")
                max_energy = energy
    logger.info("Part 2: %d", max_energy)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
