"""
Author: Nat with Darren's Template
Date: 2023-12-03

Solving https://adventofcode.com/2023/day/3

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 3

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

    logger.debug("lines %s", len(data))
    parts = []
    gears = []
    # find parts
    for row, line in enumerate(data):
        for col, c in enumerate(line):
            if c != "." and not c.isdigit():
                # logger.debug("c at %s: %s", col, c)
                parts.append(ac.Point(row, col))
                if c == "*":
                    gears.append(ac.Point(row, col))
    # logger.debug("part %s", parts)
    part1 = 0
    # find adjacent number
    gear_dict = {gear: [] for gear in gears}
    for row, line in enumerate(data):
        current_number = None
        number_start = None
        valid_part = False
        gear_part = None
        line_parts = []
        for col, c in enumerate(line):
            if c.isdigit():
                if number_start == None:
                    number_start = col
                    current_number = int(c)
                else:
                    current_number *= 10
                    current_number += int(c)
                if not valid_part:
                    for look in ac.Point(row, col).yield_neighbours():
                        if look in parts:
                            valid_part = True
                            if look in gears:
                                gear_part = look
                            # break

            else:
                if current_number:
                    if valid_part:
                        line_parts.append((number_start, col, current_number))
                        part1 += current_number
                    if gear_part:
                        gear_dict[gear_part].append(current_number)
                        gear_part = None
                    number_start = None
                    current_number = None
                    valid_part = False
        if current_number and valid_part:
            part1 += current_number
            line_parts.append((number_start, col, current_number))
            number_start = None
            current_number = None
        # logger.debug("line_parts %s", line_parts)
    logger.info("part1 %s", part1)

    logger.debug("gears %s", gear_dict)
    part2 = 0
    for gear in gear_dict:
        if len(gear_dict[gear]) == 2:
            part2 += gear_dict[gear][0] * gear_dict[gear][1]
        if len(gear_dict[gear]) < 2:
            logger.debug("found3 %s", gear_dict[gear])
    logger.info("part2 %s", part2)
    # 80071063 too low


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
