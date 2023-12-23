"""
Author: Nat with Darren's Template
Date: 2023-12-23

Solving https://adventofcode.com/2023/day/23

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 23

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
    paths = dict()
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] != "#":
                paths[(x, y)] = data[y][x]
    start = (1, 0)
    goal = (len(data[0]) - 2, len(data) - 1)
    logger.debug(f"start: {start}, goal: {goal}")
    assert paths[start] == "."
    assert paths[goal] == "."

    max_steps = 0
    queue = [(start, set())]
    visited = {}
    valid_direction = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
    while queue:
        pos, hike = queue.pop(0)
        distance = len(hike)
        # logger.debug(f"at {pos} after {distance} steps")
        # logger.debug(queue)
        # have we been here on a longer hike?
        if visited.get(pos, 0) > distance:
            continue
        # if pos in visited:
        #     logger.debug(f"already been here in {visited[pos]} steps, now {distance}")
        visited[pos] = distance
        if pos == goal:
            logger.debug(f"goal reached in {distance} steps")
            if distance > max_steps:
                max_steps = distance
                logger.debug(f"new max steps: {max_steps}")
            continue
        # let's see where we can hike
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            next_pos = (pos[0] + dx, pos[1] + dy)
            if next_pos not in paths:  # not here
                continue
            if next_pos in hike:  # already been here
                continue
            # follow hills the right way
            if paths[next_pos] != "." and not valid_direction[paths[next_pos]] == (
                dx,
                dy,
            ):
                # logger.debug(
                #     "not a valid direction at %s: %s going %s",
                #     next_pos,
                #     paths[next_pos],
                #     (dx, dy),
                # )
                continue
            # if we've been here before, check if we can do better
            if next_pos in visited and visited[next_pos] > distance + 1:
                continue
            hike_cont = hike.copy()
            hike_cont.add(pos)
            queue.append((next_pos, hike_cont))
    logger.info("Part 1: %s", max_steps)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
