"""
Author: Nat with Darren's Template
Date: 2023-12-02

Solving https://adventofcode.com/2023/day/2

Part 1: find the sum of the game ids that exceed the threshold

Part 2: find the product of the minimums of each color

"""
import logging
import time
import aoc_common.aoc_commons as ac
from functools import reduce
import operator

YEAR = 2023
DAY = 2

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

# 12 red cubes, 13 green cubes, and 14 blue cubes
threshold = {"red": 12, "green": 13, "blue": 14}


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)

    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    sum_game_ids = 0
    sum_game_powers = 0
    for line in data:
        minimums = {color: 0 for color in threshold.keys()}
        left, right = line.split(":")
        game_id = int(left.split(" ").pop())
        # logger.debug("game_id %s", game_id)
        reveals = right.strip().split(";")
        # part 1: check for a reveal exceeding threshold
        exceed = False
        for reveal in reveals:
            cubes = reveal.split(",")
            for cube in cubes:
                count, color = cube.strip().split(" ")
                if int(count) > threshold[color]:
                    logger.debug("Game %s exceeds: %s", game_id, reveal)
                    exceed = True
                if int(count) > minimums[color]:
                    minimums[color] = int(count)
        # part 2: power is product of minimums
        game_power = reduce(operator.mul, minimums.values(), 1)
        logger.debug("game_power %s", game_power)
        sum_game_powers += game_power
        if not exceed:
            sum_game_ids += game_id
    logger.info("Part 1: %s", sum_game_ids)
    logger.info("Part 2: %s", sum_game_powers)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
