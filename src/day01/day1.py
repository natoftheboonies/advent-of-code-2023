"""
Author: Nat with Darren's template
Date: 2023-12-01

Solving https://adventofcode.com/2023/day/1

Part 1: easy find-the-numbers.

Part 2: now some numbers are words.  search/replace doesn't work 
as some words are substrings of other words.

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 1

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def part1():
    # with open(locations.sample_input_file, mode="rt") as f:
    with open(locations.input_file, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)

    solution = 0
    for line in data:
        nums = []
        for char in line:
            if char.isdigit():
                nums.append(int(char))
        val = nums[0] * 10 + nums[-1]
        logger.debug(val)
        solution += val
    logger.info("Part 1: %s", solution)
    assert solution == 54239


replace = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def calibration(line):
    """
    find all numbers
    find all words to replace with numbers
    return 10 * first number + last number
    """
    i = 0
    nums = []
    while i < len(line):
        if line[i].isdigit():
            nums.append(int(line[i]))

        for match in replace:
            if line[i:].startswith(match):
                nums.append(replace[match])
        i += 1
    return 10 * nums[0] + nums[-1]


def part2():
    with open(locations.input_file, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)

    solution = 0
    for line in data:
        logger.debug(line)
        val = calibration(line)
        logger.debug(val)
        solution += val
    logger.info("Part 2: %s", solution)
    assert solution == 55343


def main():
    part1()
    part2()


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
