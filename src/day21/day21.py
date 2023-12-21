"""
Author: Nat with Darren's Template
Date: 2023-12-21

Solving https://adventofcode.com/2023/day/21

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 21

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
    grid = []
    for line in data:
        grid.append(list(line))
        if "S" in line:
            start = (line.index("S"), len(grid) - 1)
            grid[-1][start[0]] = "."
    logger.debug("start: %s", start)

    last = [start]
    NUM_STEPS = 64 if len(grid) == 131 else 6
    for _ in range(NUM_STEPS):
        plots = set()
        for x, y in last:
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if grid[y + dy][x + dx] == ".":
                    plots.add((x + dx, y + dy))
        # logger.debug(plots)
        last = plots
    logger.info("Part 1: %s", len(plots))

    def find_factors(num):
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        return factors

    PART2_STEPS = 26501365
    # factor part2_steps
    # logger.debug("part2_factors: %s", find_factors(part2_steps))
    assert 5 * 11 * 481843 == PART2_STEPS
    logger.debug("grid size: %d x %d", len(grid), len(grid[0]))

    # yeah I don't know how to do this.  help me reddit!
    # https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keavm0j/?context=3
    ROWS = len(data)
    COLS = len(data[0])

    plots = {
        (i, j) for i in range(ROWS) for j in range(len(data[i])) if data[i][j] in ".S"
    }
    S = next(
        (i, j) for i in range(ROWS) for j in range(len(data[i])) if data[i][j] == "S"
    )
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def tadd(a, b):
        return ((a[0] + b[0]), (a[1] + b[1]))

    def modp(a):
        return (a[0] % COLS, a[1] % ROWS)

    visited, new, cache = {S}, {S}, {0: 1}
    k, r = PART2_STEPS // ROWS, PART2_STEPS % ROWS
    logger.debug("n %d, k %d, r %d", ROWS, k, r)

    # P(x) = a*x**2 + b*x + c:
    # c = P(0)
    # a = (P(2) + c - 2*P(1)) / 2
    # b = P(1) - c -a

    for c in range(1, r + 2 * ROWS + 1):
        visited, new = new, {
            np
            for p in new
            for di in dirs
            for np in [tadd(p, di)]
            if np not in visited and modp(np) in plots
        }

        cache[c] = len(new) + (cache[c - 2] if c > 1 else 0)

    d2 = cache[r + 2 * ROWS] + cache[r] - 2 * cache[r + ROWS]
    d1 = cache[r + 2 * ROWS] - cache[r + ROWS]
    for step in [6, 10, 50]:
        logger.debug("step %d: %d", step, cache[step])
    part2 = cache[r + 2 * ROWS] + (k - 2) * (2 * d1 + (k - 1) * d2) // 2
    logger.info("Part 2: %s", part2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
