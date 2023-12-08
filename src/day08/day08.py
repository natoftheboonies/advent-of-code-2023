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

YEAR = 2023
DAY = 8

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
    steps = list(data[0])
    logger.debug(steps)
    assert data[1] == ""
    junctions = {}
    for row in data[2:]:
        left, right = row.split(" = ")
        right = right[1:-1].split(", ")

        junctions[left] = right
    logger.debug(junctions)
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
    logger.debug("Part 1: %d", len(followed))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
