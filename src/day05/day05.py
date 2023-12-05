"""
Author: Nat with Darren's Template
Date: 2023-12-05

Solving https://adventofcode.com/2023/day/5

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 5

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

    logger.debug(data)
    seeds = [int(seed) for seed in data[0].split(":")[1].strip().split()]
    logger.debug(seeds)
    maps = {}
    map_sequence = []
    current_map = None
    for line in data[1:]:
        if line.strip().endswith("map:"):
            current_map = []
            maps[line] = current_map
            map_sequence.append(line)
        else:
            if line.strip() == "":
                continue
            mapping = [int(n) for n in line.strip().split(" ")]
            assert len(mapping) == 3
            current_map.append(mapping)
    logger.debug(maps)

    minimum_location = 1e9

    for seed in seeds:
        seed_ids = [seed]
        for map in map_sequence:
            last = seed_ids[-1]
            for dest, source, length in maps[map]:
                # dest, source, length
                if last >= source and last <= source + length:
                    seed_ids.append(dest + last - source)
                    break
            else:
                seed_ids.append(last)
        logger.debug(seed_ids)
        minimum_location = min(minimum_location, seed_ids[-1])
    logger.info("Part 1: %d", minimum_location)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
