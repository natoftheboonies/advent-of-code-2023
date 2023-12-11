"""
Author: Nat with Darren's Template
Date: 2023-12-11

Solving https://adventofcode.com/2023/day/11

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 11

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
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

    # logger.debug(data)
    galaxies = []
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == ".":
                continue
            galaxies.append((x, y))
    logger.debug("galaxies %d", len(galaxies))

    max_y = len(data)
    max_x = len(data[0])
    expand_x = []
    expand_y = []
    for i in range(max_x):
        if not any(True for x, _ in galaxies if x == i):
            expand_x.append(i)
    for i in range(max_y):
        if not any(True for _, y in galaxies if y == i):
            expand_y.append(i)
    logger.debug("expand x %s", expand_x)
    logger.debug("expand y %s", expand_y)
    # compare pairs of galaxies, ignoring order
    sum_part1 = 0
    sum_part2 = 0
    for i in range(len(galaxies)):
        x1, y1 = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            x2, y2 = galaxies[j]
            dist = abs(x1 - x2) + abs(y1 - y2)
            sum_part1 += dist
            sum_part2 += dist
            sum_part1 += sum(1 for x in expand_x if min(x1, x2) < x < max(x1, x2))
            sum_part2 += sum(1e6 - 1 for x in expand_x if min(x1, x2) < x < max(x1, x2))
            sum_part1 += sum(1 for y in expand_y if min(y1, y2) < y < max(y1, y2))
            sum_part2 += sum(1e6 - 1 for y in expand_y if min(y1, y2) < y < max(y1, y2))
            # logger.debug("dist %s: %d", (i + 1, j + 1), dist)
    logger.info("Part 1 %d", sum_part1)
    logger.info("Part 2 %d", sum_part2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
