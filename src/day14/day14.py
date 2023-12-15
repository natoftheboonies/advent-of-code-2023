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
logger.setLevel(logging.INFO)
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
    for row in data:
        logger.debug("".join(row))

    for y, row in enumerate(data):
        for _, col in enumerate(row):
            if col == "O":
                platform_sum += len(data) - y

    logger.info("Part 1: %s", platform_sum)
    cycle = 0
    total_cycles = int(1e9)
    cycle_history = {}
    detected_cycle = False
    while cycle < total_cycles:
        data = tilt_west(data)
        data = tilt_south(data)
        data = tilt_east(data)
        cycle += 1

        platform_sum = 0
        for y, row in enumerate(data):
            for _, col in enumerate(row):
                if col == "O":
                    platform_sum += len(data) - y
        logger.debug("cycle %d %d", cycle, platform_sum)

        # cycle detection
        state = "".join(["".join(row) for row in data])
        if not detected_cycle and state in cycle_history:
            detected_cycle = True
            cycle_length = cycle - cycle_history[state]
            logger.debug("cycle length %d", cycle_length)
            # skip until just before end
            skip_ahead = (total_cycles - cycle) // cycle_length * cycle_length
            cycle += skip_ahead
            logger.debug("skipping %d cycles until %d", skip_ahead, cycle)

        cycle_history[state] = cycle
        data = tilt_north(data)

    logger.info("Part 2: %d", platform_sum)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
