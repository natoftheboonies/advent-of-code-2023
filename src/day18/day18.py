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
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


# https://en.wikipedia.org/wiki/Shoelace_formula
def shoelace(coords):
    area = 0
    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        area += x1 * y2 - x2 * y1
    return abs(area) // 2


def solve(inst):
    lagoon = []
    current = (0, 0)
    lagoon.append(current)
    outline = 0

    for d, n in inst:
        if d == "U":
            current = (current[0], current[1] + n)
        elif d == "D":
            current = (current[0], current[1] - n)
        elif d == "R":
            current = (current[0] + n, current[1])
        elif d == "L":
            current = (current[0] - n, current[1])
        else:
            raise ValueError(f"Unknown direction {d}")
        lagoon.append(current)
        outline += n
    area = shoelace(lagoon)
    logger.debug("area: %d", area)
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # A = i + b/2 - 1
    # but we don't want area, we want interior + boundary points.  i+b
    # and we have outline, which is b
    # i = A + 1 - b/2
    i = area + 1 - outline // 2
    return i + outline


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

    logger.info("Part 1: %d", solve(inst))

    # Part 2
    decode = {
        0: "R",
        1: "D",
        2: "L",
        3: "U",
    }
    inst = []
    for line in data:
        d, n, color = line.strip().split()
        color = color[2:-1]
        n = int(color[:-1], base=16)
        d = decode[int(color[-1])]
        logger.debug(f"{d} {n}")
        inst.append((d, n))
    logger.info("Part 2: %d", solve(inst))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
