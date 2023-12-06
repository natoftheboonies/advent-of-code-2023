"""
Author: Nat with Darren's Template
Date: 2023-12-06

Solving https://adventofcode.com/2023/day/6

Part 1:

Part 2: binary search

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 6

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

    logger.debug(data)
    times = [int(n) for n in data[0].split()[1:]]
    distances = [int(n) for n in data[1].split()[1:]]
    product = 1
    for n in range(len(times)):
        time = times[n]
        goal = distances[n]
        count = 0
        for i in range(1, (time + 1) // 2):
            if i * (time - i) > goal:
                count += 1
        count *= 2
        if time % 2 == 0:
            count += 1
        logger.debug("c: %d", count)
        product *= count
    logger.info("Part 1: %d", product)

    # Part 2
    time = int("".join(data[0].split()[1:]))
    logger.debug("t: %d", time)
    distance = int("".join(data[1].split()[1:]))
    logger.debug("d: %d", distance)
    # binary search ftw!
    low = 0
    middle = (time + 1) // 2
    high = middle
    while low < high:
        mid = (low + high) // 2
        if mid * (time - mid) < distance:
            low = mid + 1
        else:
            high = mid
    logger.debug("crossover: %d", low)
    result = 2 * (middle - low)
    if time % 2 == 0:
        result += 1
    logger.info("Part 2: %d", result)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
