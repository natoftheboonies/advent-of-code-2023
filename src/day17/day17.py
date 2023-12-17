"""
Author: Nat with Darren's Template
Date: 2023-12-17

Solving https://adventofcode.com/2023/day/17

Part 1:

Part 2:

"""
from enum import Enum
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 17

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


class Heading(Enum):
    E = (1, 0)
    W = (-1, 0)
    N = (0, -1)
    S = (0, 1)

    def turn_left(self):
        return Heading((self.value[1], -self.value[0]))

    def turn_right(self):
        return Heading((-self.value[1], self.value[0]))

    def move(self, x, y, distance=1):
        return (x + self.value[0] * distance, y + self.value[1] * distance, self)

    def valid_next(self, count=0):
        if count == 3:
            return [self.turn_left(), self.turn_right()]
        assert count < 3
        return [self, self.turn_left(), self.turn_right()]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def main():
    puzzle = locations.input_file
    puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        # data = [list(map(int, list(line))) for line in f.read().splitlines()]
        data = [[int(n) for n in list(line)] for line in f.read().splitlines()]

    logger.debug(ac.top_and_tail(data))

    # state is position, heading, heat
    # never need to re-visit a position? of course we do. we need to re-visit a position if we can get there with a lower heat
    visited = dict()  # (x, y, heading) -> heat
    # x, y, heading, count, heat
    pos = (0, 0, Heading.E, 1, 0)
    queue = []
    queue.append(pos)
    goal = (len(data[0]) - 1, len(data) - 1)
    min_heat = 10**10
    while queue:
        x, y, heading, count, heat = queue.pop(0)
        # logger.debug(f"({x},{y}) {heading}")
        if x < 0 or x >= len(data[0]) or y < 0 or y >= len(data):
            continue
        if (x, y, heading) in visited and visited.get((x, y, heading), 10**10) < heat:
            continue
        visited[(x, y, heading)] = heat
        if (x, y) == goal:
            logger.info(f"Found goal at ({x},{y}) with heat {heat}")
            min_heat = min(min_heat, heat)
        for h in heading.valid_next(count):
            dx, dy, _ = h.move(x, y)
            if h == heading:
                queue.append((dx, dy, h, count + 1, heat + data[y][x]))
            else:
                queue.append((dx, dy, h, 1, heat + data[y][x]))
    logger.debug("Part 1: %d", min_heat)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
