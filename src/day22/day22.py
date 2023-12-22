"""
Author: Nat with Darren's Template
Date: 2023-12-22

Solving https://adventofcode.com/2023/day/22

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 22

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def print_column(column):
    min_z = min([z for _, _, z in column.keys()])
    max_z = max([z for _, _, z in column.keys()])
    min_x = min([x for x, _, _ in column.keys()])
    max_x = max([x for x, _, _ in column.keys()])
    min_y = min([y for _, y, _ in column.keys()])
    max_y = max([y for _, y, _ in column.keys()])

    logger.debug("x vs z")
    for z in range(max_z, min_z - 1, -1):
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y, z) in column:
                    print(column[(x, y, z)], end="")
                    break
            else:
                print(".", end="")
        print()
    logger.debug("y vs z")
    for z in range(max_z, min_z - 1, -1):
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y, z) in column:
                    print(column[(x, y, z)], end="")
                    break
            else:
                print(".", end="")
        print()


def bricks_overlap(brick, other):
    x_overlaps = max(brick[0][0], other[0][0]) <= min(brick[1][0], other[1][0])
    y_overlaps = max(brick[0][1], other[0][1]) <= min(brick[1][1], other[1][1])
    return x_overlaps and y_overlaps


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()
    bricks = []
    for line in data:
        left, right = line.split("~")
        left = list(int(x) for x in left.split(","))
        right = list(int(x) for x in right.split(","))
        bricks.append((left, right))
        assert left[0] <= right[0]
        assert left[1] <= right[1]
        assert left[2] <= right[2]
        assert left[2] > 0

    bricks.sort(key=lambda x: x[0][2])
    logger.debug(bricks[:3])  # minimum brick(s) at z = 1

    # now simulate gravity.
    for i, brick in enumerate(bricks):
        if i == 0:
            continue
        fall_to_z = 1  # 0 is ground
        # logger.debug("falling brick: %s", brick)
        # find lower bricks which overlap and update fall_to_z value.
        for brick2 in bricks[:i]:
            if bricks_overlap(brick, brick2):
                # logger.debug("falling brick overlaps with: %s", brick2)
                fall_to_z = max(fall_to_z, brick2[1][2] + 1)  # top of brick2 + 1
            brick[1][2] -= brick[0][2] - fall_to_z
            brick[0][2] = fall_to_z

            # logger.debug("fell to: %s", brick)

    bricks.sort(key=lambda x: x[0][2])
    logger.debug(bricks)

    # find bricks supported by >1 brick
    brick_supporting = {i: [] for i in range(len(bricks))}
    brick_supported_by = {i: [] for i in range(len(bricks))}
    for i, brick in enumerate(bricks):  # upper bricks
        for j, brick2 in enumerate(bricks[:i]):  # lower bricks
            if bricks_overlap(brick, brick2) and brick[0][2] == brick2[1][2] + 1:
                brick_supporting[j].append(i)
                brick_supported_by[i].append(j)

    logger.debug(brick_supported_by)

    count = 0
    for i, brick in enumerate(bricks):
        logger.debug("considering brick %s", i)
        for j in brick_supporting[i]:
            if len(brick_supported_by[j]) <= 1:
                logger.debug("brick %s is supported by single", j)
                break
        else:
            count += 1

    logger.info("Part 1: %d", count)

    # Part 2
    count = 0

    for i in range(len(bricks)):
        logger.debug("removing brick %s", i)
        falling = []
        # if we remove brick i, what else will fall?  start with bricks supported by only i
        cascade = [j for j in brick_supporting[i] if brick_supported_by[j] == [i]]
        falling.extend(cascade)
        logger.debug("directly falling bricks: %s", falling)
        # now remove thos bricks and see what else falls
        while len(cascade) > 0:
            j = cascade.pop()
            for k in brick_supporting[j]:
                if k in falling:
                    continue
                if all(l in falling or l == i for l in brick_supported_by[k]):
                    logger.debug("brick %s also falling", k)
                    cascade.append(k)
                    falling.append(k)
        logger.debug("total falling bricks: %s", falling)
        count += len(falling)
    logger.info("Part 2: %d", count)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
