"""
Author: Nat with Darren's Template
Date: 2023-12-09

Solving https://adventofcode.com/2023/day/9

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 9

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def part1(sequence):
    next = []
    i = 1
    while i < len(sequence):
        next.append(sequence[i] - sequence[i - 1])
        i += 1
    logger.debug(next)
    if all(x == 0 for x in next):
        logger.debug("base: %d", sequence[-1])
        return sequence[-1]  # same for part 2
    result = sequence[-1] + part1(next)

    logger.debug("next: %d", result)
    return result


def part2(sequence):
    next = []
    i = 1
    while i < len(sequence):
        next.append(sequence[i] - sequence[i - 1])
        i += 1
    logger.debug(next)
    if all(x == 0 for x in next):
        logger.debug("base: %d", sequence[0])
        return sequence[0]
    result = sequence[0] - part2(next)
    logger.debug("next: %d", result)
    return result


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    sum_results = 0

    logger.debug(data)
    for line in data:
        sequence = list(map(int, line.split()))
        logger.debug(sequence)
        sum_results += part1(sequence)

    logger.info("Part 1: %d", sum_results)
    sum_results = 0
    for line in data:
        sequence = list(map(int, line.split()))
        logger.debug(sequence)
        sum_results += part2(sequence)

    logger.info("Part 2: %d", sum_results)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
