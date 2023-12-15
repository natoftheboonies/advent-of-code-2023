"""
Author: Nat with Darren's Template
Date: 2023-12-15

Solving https://adventofcode.com/2023/day/15

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 15

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def hash(data):
    current = 0
    for v in data:
        current += ord(v)
        current *= 17
        current %= 256
    return current


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    data = data[0].split(",")
    total = 0
    for i in data:
        total += hash(i)
    logger.info("Part 1: %d", total)

    # Part 2
    hashmap = {}
    for i, v in enumerate(data):
        if "-" in v:
            assert v[-1] == "-"
            label = v[:-1]
            key = hash(label)
            if key in hashmap:
                index = None
                for j, (lens, _) in enumerate(hashmap[key]):
                    if lens == label:
                        index = j
                        break
                if index is not None:
                    logger.debug("Removing %s from %s", label, hashmap[key])
                    del hashmap[key][index]
        elif "=" in v:
            label, focus = v.split("=")
            focus = int(focus)
            key = hash(label)
            if key not in hashmap:
                hashmap[key] = [(label, focus)]
            else:
                for j, (lens, _) in enumerate(hashmap[key]):
                    if lens == label:
                        logger.debug("Replacing %s from %s", label, hashmap[key])
                        hashmap[key][j] = (label, focus)
                        break
                else:
                    hashmap[hash(label)].append((label, focus))
        logger.debug(hashmap)

    part2 = 0
    for key in hashmap:
        for idx, (label, focus) in enumerate(hashmap[key]):
            power = 1 * (key + 1) * (idx + 1) * focus
            logger.debug("power %s: %d", label, power)
            part2 += power

    logger.info("Part 2: %d", part2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
