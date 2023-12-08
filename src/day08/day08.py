"""
Author: Nat with Darren's Template
Date: 2023-12-08

Solving https://adventofcode.com/2023/day/8

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
from math import gcd

YEAR = 2023
DAY = 8

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def part1(steps, junctions):
    current = "AAA"
    step_idx = 0
    followed = [current]
    assert current in junctions
    while True:
        logger.debug(f"{current} : {steps[step_idx]}")
        if steps[step_idx] == "R":
            current = junctions[current][1]
        elif steps[step_idx] == "L":
            current = junctions[current][0]
        else:
            raise ValueError(f"Unknown step {steps[step_idx]}")
        step_idx += 1
        step_idx %= len(steps)
        if current == "ZZZ":
            break
        followed.append(current)

    assert current == "ZZZ"
    logger.info("Part 1: %d", len(followed))


def explore_from_a_start(start, steps, junctions, ends_in_Z):
    # how long until we get back to ZZZ?
    current = start
    step_idx = 0
    step_count = 0
    visits = []
    while len(visits) < 5:
        if steps[step_idx] == "R":
            current = junctions[current][1]
        elif steps[step_idx] == "L":
            current = junctions[current][0]
        else:
            raise ValueError(f"Unknown step {steps[step_idx]}")
        step_idx += 1
        step_idx %= len(steps)
        step_count += 1
        if current in ends_in_Z:
            # logger.debug("ZZZ at step %d", step_count)
            visits.append(step_count)

    return visits


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)
    steps = list(data[0])
    logger.debug(steps)
    assert data[1] == ""
    junctions = {}
    for row in data[2:]:
        left, right = row.split(" = ")
        right = right[1:-1].split(", ")

        junctions[left] = right
    logger.debug(junctions)
    part1(steps, junctions)

    # Part 2
    ends_in_A = [loc for loc in junctions if loc.endswith("A")]
    ends_in_Z = [loc for loc in junctions if loc.endswith("Z")]
    logger.debug(ends_in_A)
    logger.debug(ends_in_Z)

    periods = []
    for start in ends_in_A:
        logger.debug(f"Start at {start}")
        visits = explore_from_a_start(start, steps, junctions, ends_in_Z)
        logger.debug(visits)
        # find period of visits
        period = visits[1] - visits[0]
        assert visits[2] - visits[1] == period
        assert visits[3] - visits[2] == period
        assert visits[4] - visits[3] == period
        periods.append(period)
    # find the LCM of the periods
    lcm = 1
    for period in periods:
        lcm = lcm * period // gcd(lcm, period)
    logger.info("Part 2: %d", lcm)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return (a * b) // gcd(a, b)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
