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

    valid_direction = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

    junctions = set([start, goal])
    for pos in paths:
        if paths[pos] != ".":
            dirs = [valid_direction[paths[pos]]]
        else:
            dirs = valid_direction.values()
        exits = 0
        for dx, dy in dirs:
            if (pos[0] + dx, pos[1] + dy) in paths:
                exits += 1
        if exits > 2:
            junctions.add(pos)

    compressed = {junction: dict() for junction in junctions}
    for junction in junctions:
        queue = [(junction, 0)]
        visited = set(junction)
        while queue:
            pos, distance = queue.pop(0)
            if pos in junctions and pos != junction:
                compressed[junction][pos] = distance
                continue
            explore = valid_direction.values()
            if paths[pos] != ".":  # we're on a hill
                explore = [valid_direction[paths[pos]]]
            for dx, dy in explore:
                next_pos = (pos[0] + dx, pos[1] + dy)
                if next_pos not in paths or next_pos in visited:
                    continue
                queue.append((next_pos, distance + 1))
                visited.add(next_pos)

    logger.debug("compressed %s", compressed)

    max_steps = 0
    queue = [(start, set(), 0)]
    visited = {}

    while queue:
        pos, hike, distance = queue.pop(0)
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
        for next_pos in compressed[pos]:
            if next_pos in hike:  # already been here
                continue
            next_distance = compressed[pos][next_pos]
            # if we've been here before, check if we can do better
            if next_pos in visited and visited[next_pos] > distance + next_distance:
                continue
            hike_cont = hike.copy()
            hike_cont.add(pos)
            queue.append((next_pos, hike_cont, distance + next_distance))
    logger.info("Part 1: %s", max_steps)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
