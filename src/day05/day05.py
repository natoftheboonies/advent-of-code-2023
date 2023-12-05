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
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def map_seed_ranges(seed_ranges, current_map):
    output_ranges = []
    for start, end in seed_ranges:
        logger.debug("input: %s", (start, end))
        for dest, source, length in current_map:
            source_end = source + length
            # fully contained
            if start >= source and end <= source_end:
                new_start = dest + start - source
                new_end = dest + end - source
                logger.debug(
                    "full transformation: %s -> %s", (start, end), (new_start, new_end)
                )
                output_ranges.append((new_start, new_end))
                break
            # partially_contained
            elif start < source and end > source:
                logger.debug(
                    "partial transformation, low %s -> %s",
                    (start, end),
                    (source, source_end),
                )
                logger.debug("dest, source, length: %s", (dest, source, length))
                # extract off the matching part, but continue
                # (2, 8) & (5, 10) => (2, 5) & (5, 8)
                # st, en & so, se => st, so & so, en
                sub_start = start  # 2
                sub_end = source  # 5
                match_start = source  # 5
                match_end = end  # 8
                new_start = dest  # + match_start - source
                new_end = dest + match_end - source
                logger.debug(
                    "transformed %s -> %s",
                    (start, end),
                    (new_start, new_end),
                )
                output_ranges.append((new_start, new_end))
                start = sub_start
                end = sub_end
            elif start < source_end and end > source_end:
                logger.debug(
                    "partial transformation, high %s -> %s",
                    (start, end),
                    (source, source_end),
                )
                logger.debug("dest, source, length: %s", (dest, source, length))
                # extract off the matching part, but continue
                # (8, 12) & (5, 10) => (8, 10) & (10, 12)
                # st, en & so, se => st, se & se, en
                sub_start = source_end  # 10
                sub_end = end  # 12
                match_start = start  # 8
                match_end = source_end  # 10
                new_start = dest + match_start - source
                new_end = dest + match_end - source
                logger.debug(
                    "transformed %s -> %s",
                    (start, end),
                    (new_start, new_end),
                )
                output_ranges.append((new_start, new_end))
                # retain rest of range for further matching
                start = sub_start
                end = sub_end
        else:
            logger.debug("no transformation in %s", (start, end))
            output_ranges.append((start, end))
    output_ranges = sorted(output_ranges)
    logger.debug("outputs: %s", output_ranges)
    return output_ranges


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
                if last >= source and last < source + length:
                    seed_ids.append(dest + last - source)
                    break
            else:
                # did not map, pass through
                seed_ids.append(last)
        logger.debug(seed_ids)
        minimum_location = min(minimum_location, seed_ids[-1])
    logger.info("Part 1: %d", minimum_location)
    # 403695602

    # Part 2... well, we can't just explore the whole space!
    # instead, ranges.
    # split seeds into pairs:
    seed_ranges = sorted(
        [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    )

    logger.debug("seed ranges: %s", seed_ranges)  # >= a and < b
    for map in map_sequence:
        logger.debug(map)
        seed_ranges = map_seed_ranges(seed_ranges, maps[map])

    logger.debug(seed_ranges)
    # find the transformations for each input range
    logger.info("Part 2: %d ", seed_ranges[0][0])
    # 324294413 too high


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
