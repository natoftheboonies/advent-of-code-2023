"""
Author: Darren
Date: 01/12/2023

Solving https://adventofcode.com/2023/day/1

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
import re

YEAR = 2023
DAY = 1

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
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
        nums = list(map(int, re.findall(r"\d", line)))
        val = nums[0] * 10 + nums[-1]
        logger.debug(val)
        solution += val
    logger.info("Part 1: %s", solution)

    # solution = 0
    # logger.info("Part 2: %s", solution)


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
    "oneight": 8,
}


def translate(string):
    i = 0
    transl = ""
    while i < len(string):
        if string[i].isdigit():
            transl += string[i]

        for match in replace.keys():
            if string[i:].startswith(match):
                transl += str(replace[match])
        i += 1
    return transl


def part2():
    with open(locations.input_file, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)

    # sevenine, eightwo, nineight, oneight, threeight

    string = "ggdone3nbmsthreefourninefiveoneightpr"
    logger.debug(translate(string))

    # find all words to replace
    # find all numbers
    # replace words with numbers

    solution = 0
    count = 0
    for line in data:
        logger.debug(line)
        line = translate(line)
        nums = list(map(int, re.findall(r"\d", line)))
        val = nums[0] * 10 + nums[-1]
        logger.debug(val)
        solution += val
    # if count == 106:
    #     break
    logger.info("Part 2: %s", solution)
    # not 55330, 55743

    # solution = 0
    # logger.info("Part 2: %s", solution)


def main():
    part2()


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
