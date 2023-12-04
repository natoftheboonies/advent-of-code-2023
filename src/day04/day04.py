"""
Author: Nat with Darren's Template
Date: 2023-12-04

Solving https://adventofcode.com/2023/day/4

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
import re

YEAR = 2023
DAY = 4

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
    total_score = 0
    logger.debug(data)
    for line in data:
        parts = re.match(
            r"Card\s+(\d+): \s?((?:\d+\s+)+)\| \s?((?:\d+\s*)+)", line.strip()
        )
        if not parts:
            logger.error("No match for %s", line)
            continue
        card, winning, played = parts.groups()
        winning = [int(x) for x in winning.split()]
        played = [int(x) for x in played.split()]
        matches = [1 for x in played if x in winning]
        logger.debug(matches)
        if len(matches) > 0:
            score = 0
            score = 2 ** (len(matches) - 1)
            logger.debug(score)
            total_score += score

    logger.info("Total score: %d", total_score)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
