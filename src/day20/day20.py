"""
Author: Nat with Darren's Template
Date: 2023-12-20

Solving https://adventofcode.com/2023/day/20

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
from collections import deque

YEAR = 2023
DAY = 20

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
    modules = {}
    broadcast = []
    for line in data:
        left, right = line.split(" -> ")
        logger.debug(f"{left} -> {right}")
        if "," in right:
            right = right.split(", ")
        if left[0] in "&%":
            left = (left[0], left[1:])
            modules[left[1]] = (left[0], right)
        else:
            assert left == "broadcaster"
            broadcast = right
    logger.debug(f"{modules.keys()}")

    low_pulses = 1  # button to broadcaster
    high_pulses = 0
    # button sends to broadcaster
    queue = deque([])
    for module in broadcast:
        low_pulses += 1
        queue.append(modules[module])
    logger.debug(f"{queue}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
