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
        for x, c in enumerate(row):
            if c == ".":
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


def tilt_south(data):
    for y in range(len(data) - 1, 0, -1):
        for x, c in enumerate(data[y]):
            if c == ".":
                # look for a round above
                for i in range(y - 1, -1, -1):
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
    for x in range(len(data[0]) - 1, 0, -1):
        for y in range(len(data)):
            c = data[y][x]
            if c == ".":
                # look for a round west
                for i in range(x - 1, -1, -1):
                    if data[y][i] == ".":
                        continue
                    else:
                        if data[y][i] == "O":
                            data[y][x] = data[y][i]
                            data[y][i] = "."
                        else:
                            assert data[y][i] == "#"
                        break
    return data


def tilt_west(data):  # left
    for x in range(len(data[0])):
        for y in range(len(data)):
            c = data[y][x]
            if c == ".":
                # look for a round east
                for i in range(x + 1, len(data[0])):
                    if data[y][i] == ".":
                        continue
                    else:
                        if data[y][i] == "O":
                            data[y][x] = data[y][i]
                            data[y][i] = "."
                        else:
                            assert data[y][i] == "#"
                        break
    return data


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = [list(line) for line in f.read().splitlines()]

    logger.debug(data)
    platform_sum = 0
    data = tilt_north(data)
    logger.info("north")
    for row in data:
        logger.debug("".join(row))

    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == "O":
                platform_sum += len(data) - y

    logger.info("Part 1: %s", platform_sum)
    total_cycles = 000000000
    cycle_history = []
    for cycle in range(1, 201):
        data = tilt_west(data)

        data = tilt_south(data)

        data = tilt_east(data)

        platform_sum = 0
        for y, row in enumerate(data):
            for x, col in enumerate(row):
                if col == "O":
                    platform_sum += len(data) - y
        cycle_history.append(platform_sum)
        if platform_sum == 102837:
            logger.debug("cycle 102837 %d", cycle)
        data = tilt_north(data)
    logger.debug("history: %s", cycle_history)
    index = (total_cycles - 93) % 7
    logger.info("Part 2: %d", cycle_history[93 + index - 2])
    part2 = 102829


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
