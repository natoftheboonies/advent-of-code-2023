"""
Author: Nat with Darren's Template
Date: 2023-12-13

Solving https://adventofcode.com/2023/day/13

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 13

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def reflected(image):
    sequence = []
    for row in image:
        row = "".join(row).replace(".", "0").replace("#", "1")
        # to decimal
        row = int(row, 2)
        sequence.append(row)
    for i, n in enumerate(sequence):
        # logger.debug("i: %s, n: %s", i, n)
        if i == 0:
            continue
        if n == sequence[i - 1]:
            logger.debug("check reflection at %d", i)
            for j in range(i, len(sequence)):
                k = i - (j - i) - 1
                if k < 0:
                    continue
                logger.debug("j: %d vs %d", sequence[j], sequence[k])
                if sequence[j] != sequence[k]:
                    break
            else:
                return i
    return -1


def analyze(image):
    # look for reflected sequence
    v = reflected(image)
    if v > 0:
        return 100 * v
    rotated = list(zip(*image[::-1]))
    h = reflected(rotated)
    if h > 0:
        return h
    logger.warn("no reflection found")


from copy import deepcopy


def part2(image):
    part1 = analyze(image)
    grid = [[c for c in row] for row in image]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            test_image = deepcopy(grid)
            test_image[y][x] = "." if grid[y][x] == "#" else "#"
            part2 = analyze(test_image)
            if part2 and part2 != part1:
                logger.debug("found smudge at %d, %d: %d", x, y, part2)
                return part2


def main():
    puzzle = locations.input_file
    puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = [image.split() for image in f.read().split("\n\n")]
    logger.debug(data)
    summarized = 0
    for image in data:
        summarized += analyze(image)
    logger.info("Part 1: %d", summarized)

    # part2 smudges?!
    summarized = 0
    for image in data:
        summarized += part2(image)
    logger.info("Part 2: %d", summarized)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
