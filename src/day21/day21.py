"""
Author: Nat with Darren's Template
Date: 2023-12-21

Solving https://adventofcode.com/2023/day/21

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 21

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
    puzzle = locations.sample_input_file

    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    grid = []
    for line in data:
        grid.append(list(line))
        if "S" in line:
            start = (line.index("S"), len(grid) - 1)
            grid[-1][start[0]] = "."
    logger.debug("start: %s", start)

    last = [start]
    NUM_STEPS = 64 if len(grid) == 131 else 6
    for _ in range(NUM_STEPS):
        plots = set()
        for x, y in last:
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if grid[y + dy][x + dx] == ".":
                    plots.add((x + dx, y + dy))
        # logger.debug(plots)
        last = plots
    logger.info("Part 1: %s", len(plots))

    def find_factors(num):
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        return factors

    part2_steps = 26501365
    # factor part2_steps
    # logger.debug("part2_factors: %s", find_factors(part2_steps))
    assert 5 * 11 * 481843 == part2_steps
    logger.debug("grid size: %d x %d", len(grid), len(grid[0]))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
