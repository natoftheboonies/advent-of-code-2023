"""
Author: Nat with Darren's Template
Date: 2023-12-04

Solving https://adventofcode.com/2023/day/4

Part 1: Points of winning lottery numbers

Part 2: Duplicate cards per points, then count cards

"""
import logging
import time
import aoc_common.aoc_commons as ac
import re

YEAR = 2023
DAY = 4

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
    total_score = 0
    logger.debug(data)
    cards = []
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
        matches = len([1 for x in played if x in winning])
        cards.append((int(card), matches))
        logger.debug(matches)
        if matches > 0:
            score = 0
            score = 2 ** (matches - 1)
            logger.debug(score)
            total_score += score

    logger.info("Part 1: %d", total_score)

    copies = {}
    for card, matches in cards:
        copies[card] = copies.get(card, 0) + 1
        if matches > 0:
            for i in range(1, matches + 1):
                card_to_copy = card + i
                copies[card_to_copy] = copies.get(card_to_copy, 0) + copies[card]
        logger.debug(copies)

    logger.info("Part 2: %d", sum(copies.values()))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
