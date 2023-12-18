"""
Author: Nat with Darren's Template
Date: 2023-12-18

Solving https://adventofcode.com/2023/day/18

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 18

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

    # logger.debug(data)
    inst = []
    for line in data:
        d, n, color = line.strip().split()
        n = int(n)
        logger.debug(f"{d} {n} {color}")
        inst.append((d, n))

    lagoon = set()
    current = (0, 0)
    for d, n in inst:
        if d == "U":
            for i in range(n):
                current = (current[0], current[1] - 1)
                lagoon.add(current)
        elif d == "D":
            for i in range(n):
                current = (current[0], current[1] + 1)
                lagoon.add(current)
        elif d == "R":
            for i in range(n):
                current = (current[0] + 1, current[1])
                lagoon.add(current)
        elif d == "L":
            for i in range(n):
                current = (current[0] - 1, current[1])
                lagoon.add(current)
        else:
            raise ValueError(f"Unknown direction {d}")

    rows = max(lagoon, key=lambda x: x[1])[1] + 1
    minrow = min(lagoon, key=lambda x: x[1])[1]
    cols = max(lagoon, key=lambda x: x[0])[0] + 1
    mincol = min(lagoon, key=lambda x: x[0])[0]
    count = 0
    for j, row in enumerate(range(minrow, rows)):
        digs = [dig[0] for dig in lagoon if dig[1] == row]
        digs.sort()
        dug = True
        thisrow = 0
        for i, dig in enumerate(digs):
            thisrow += 1
            if i == 0:
                dug = True
                continue
            # if consecutive
            if dig == digs[i - 1] + 1:
                continue
            else:  # gap
                if dug:
                    thisrow += dig - digs[i - 1] - 1
                dug = not dug
        count += thisrow
        if j % 10 == 0:
            logger.debug("%d digs: %s = %d", j + 1, digs, thisrow)
        # for col in range(mincol, cols):
        #     if (col, row) in lagoon:
        #         print("#", end="")
        #     else:
        #         print(".", end="")

        # print()

    logger.info("Part 1: %d", count)
    # 1248 low, 46131 low


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
