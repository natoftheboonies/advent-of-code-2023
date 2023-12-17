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
import heapq

YEAR = 2023
DAY = 17

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
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

    def valid_next_part2(self, count=0):
        if count < 4:
            return [self]
        if count == 10:
            return [self.turn_left(), self.turn_right()]
        assert count < 10
        return [self, self.turn_left(), self.turn_right()]

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def explore(data, next_func):
    # state is position, heading, heat
    # never need to re-visit a position? of course we do.
    # we need to re-visit a position if we can get there with a lower heat
    # or fewer turns
    visited = dict()  # (x, y, heading, count) -> heat
    # heat, x, y, heading, count
    pos = (0, 0, 0, Heading.E, 0)
    queue = []
    queue.append(pos)
    goal = (len(data[0]) - 1, len(data) - 1)
    min_heat = 10**10

    while queue:
        heat, x, y, heading, count = heapq.heappop(queue)
        # logger.debug(f"({x},{y}) {heading}")
        if (x, y, heading, count) in visited and visited[
            (x, y, heading, count)
        ] <= heat:
            continue
        visited[(x, y, heading, count)] = heat
        if (x, y) == goal:  # and count >= 4 ? why not?
            logger.debug(f"Found goal at ({x},{y},{count}) with heat {heat}")
            # return heat
            min_heat = min(min_heat, heat)
        for h in next_func(heading, count):
            nx, ny, _ = h.move(x, y)
            if nx < 0 or nx >= len(data[0]) or ny < 0 or ny >= len(data):
                continue
            new_heat = heat + data[ny][nx]
            heapq.heappush(
                queue, (new_heat, nx, ny, h, count + 1 if h == heading else 1)
            )
    return min_heat


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = [[int(n) for n in list(line)] for line in f.read().splitlines()]

    logger.debug(ac.top_and_tail(data))

    min_heat = explore(data, Heading.valid_next)
    logger.info("Part 1: %d", min_heat)

    min_heat = explore(data, Heading.valid_next_part2)
    logger.info("Part 2: %d", min_heat)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
