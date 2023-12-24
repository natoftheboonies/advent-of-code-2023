"""
Author: Nat with Darren's Template
Date: 2023-12-24

Solving https://adventofcode.com/2023/day/24

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
from math import gcd

YEAR = 2023
DAY = 24

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def cross(a, b):
    logger.debug("a: %s", a)
    logger.debug("b: %s", b)
    x0, y0, _, vx0, vy0, _ = a
    x1, y1, _, vx1, vy1, _ = b
    # x0 + vx0 * t = x1 + vx1 * t2
    # t = (x1 +vx1*t2 - x0) / vx0
    # y0 + vy0*t = y1 + vy1*t2
    # t2 = (y0 + vy0*t + y1) / vy1
    # t = (x1 +vx1*((y0 + vy0*t + y1) / vy1) - x0) / vx0
    # t * vx0 + x0 = x1 +vx1*((y0 + vy0*t + y1) / vy1)
    # t * vx0 + x0 - x1 = vx1*y0/ vy1 + vx1*vy0*t/ vy1 + vx1*y1/ vy1
    # t * vx0 - vx1*vy0*t/ vy1 = vx1*y0/ vy1 + vx1*y1/ vy1 - x0 + x1
    # t * (vx0 - vx1*vy0/ vy1) = vx1*y0/ vy1 + vx1*y1/ vy1 - x0 + x1
    # t = (vx1*y0/ vy1 + vx1*y1/ vy1 - x0 + x1) / (vx0 - vx1*vy0/ vy1)
    t1 = (vy1 * (x0 - x1) - vx1 * (y0 - y1)) / (vy0 * vx1 - vx0 * vy1)
    t2 = (vy0 * (x1 - x0) - vx0 * (y1 - y0)) / (vy1 * vx0 - vx1 * vy0)
    # logger.debug("t: %s", t1)
    # logger.debug("t: %s", t2)
    x0 = x0 + t1 * vx0
    y0 = y0 + t1 * vy0
    # logger.debug("x0: %s", x0)
    # logger.debug("y0: %s", y0)
    x1 = x1 + t2 * vx1
    y1 = y1 + t2 * vy1
    # logger.debug("x1: %s", x1)
    # logger.debug("y1: %s", y1)
    if t1 < 0 or t2 < 0:
        return None

    return x0, y0


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    stones = []
    for stone in data:
        stones.append([int(x.strip()) for x in stone.replace(" @", ",").split(",")])

    # reduce velocity by gcd:
    # for stone in stones:
    #     reduce = gcd(stone[3], stone[4])
    #     logger.debug("gcd: %s", reduce)
    #     if reduce > 1:
    #         stone[3] //= reduce
    #         stone[4] //= reduce
    #         logger.debug("reduced: %s", stone)
    logger.debug(stones)
    area_min = 7
    area_max = 27
    area_min = 200000000000000
    area_max = 400000000000000
    count = 0
    for a in stones:
        for b in stones:
            if a == b:
                continue
            if a[3] * b[4] == b[3] * a[4]:
                logger.debug("parallel: %s", a)
                logger.debug("parallel: %s", b)
                continue
            result = cross(a, b)
            if (
                result
                and area_min <= result[0] <= area_max
                and area_min <= result[1] <= area_max
            ):
                count += 1
                logger.debug("cross: %s", result)
    logger.info("Part 1: %s", count // 2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
