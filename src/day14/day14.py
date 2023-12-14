"""
Author: Nat with Darren's Template
Date: 2023-12-14

Solving https://adventofcode.com/2023/day/14

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 14

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def tilt_north(data):
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == ".":
                # look for a round below
                for i in range(y + 1, len(data)):
                    if data[i][x] == ".":
                        continue
                    else:
                        if data[i][x] == "O":
                            data[y][x] = data[i][x]
                            data[i][x] = "."
                        else:
                            assert data[i][x] == "#"
                        break
    return data


def tilt_east(data):  # right
    for x in range(len(data[0]), 0, -1):
        for y, c in enumerate(data):
            if c == ".":
                # look for a round west
                for i in range(x - 1, 0, -1):
                    if data[i][x] == ".":
                        continue
                    else:
                        if data[i][x] == "O":
                            data[y][x] = data[i][x]
                            data[i][x] = "."
                        else:
                            assert data[i][x] == "#"
                        break
    return data


def tilt_west(data):  # left
    for x in range(len(data[0])):
        for y, c in enumerate(data):
            if c == ".":
                # look for a round west
                for i in range(x + 1, len(data[0])):
                    if data[i][x] == ".":
                        continue
                    else:
                        if data[i][x] == "O":
                            data[y][x] = data[i][x]
                            data[i][x] = "."
                        else:
                            assert data[i][x] == "#"
                        break
    return data


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = [list(line) for line in f.read().splitlines()]

    logger.debug(data)
    platform_sum = 0
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == "O":
                platform_sum += len(data) - y
            if col == ".":
                # look for a round below
                for i in range(y + 1, len(data)):
                    if data[i][x] == ".":
                        continue
                    else:
                        if data[i][x] == "O":
                            data[y][x] = data[i][x]
                            data[i][x] = "."
                            platform_sum += len(data) - y
                        else:
                            assert data[i][x] == "#"
                        break
    for row in data:
        logger.debug("".join(row))
    logger.info("Part 1: %s", platform_sum)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
