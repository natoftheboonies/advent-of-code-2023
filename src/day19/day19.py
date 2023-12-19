"""
Author: Nat with Darren's Template
Date: 2023-12-19

Solving https://adventofcode.com/2023/day/19

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 19

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        rules, parts = f.read().split("\n\n")

    # parse workflows
    rules = rules.splitlines()
    rule_dict = {}
    for rule in rules:
        key, comps = rule[:-1].split("{")
        comps = comps.split(",")
        comps_parsed = []
        for comp in comps:
            left = None
            outcome = comp
            if ":" in comp:
                left, outcome = comp.split(":")
                cat = left[0]
                assert cat in "xmas"
                op = left[1]
                assert op in "<>"
                val = int(left[2:])
                left = (cat, op, val)
            comps_parsed.append((left, outcome))
        rule_dict[key] = comps_parsed
    logger.debug("Rules: %s", rule_dict)

    # parse parts
    parts = parts.splitlines()
    parts_parsed = []
    for part in parts:
        comps = part[1:-1].split(",")
        comps_parsed = {}
        for comp in comps:
            cat, val = comp.split("=")
            assert cat in "xmas"
            val = int(val)
            comps_parsed[cat] = val
        parts_parsed.append(comps_parsed)

    # logger.debug("Parts: %s", parts_parsed)

    rating_sum = 0
    for part in parts_parsed:
        logger.debug("Part: %s", part)
        workflow = "in"
        while workflow not in "AR":
            logger.debug("Workflow: %s", workflow)
            for comp in rule_dict[workflow]:
                logger.debug("Comp: %s", comp)
                left, outcome = comp
                if left is None:
                    workflow = outcome
                    break
                else:
                    cat, op, val = left
                    logger.debug("part[%s]: %s", cat, part[cat])
                    if op == "<":
                        if part[cat] < val:
                            workflow = outcome
                            break
                    elif op == ">":
                        if part[cat] > val:
                            workflow = outcome
                            break
        assert workflow in "AR"
        logger.debug("Workflow: %s", workflow)
        if workflow == "A":
            part_sum = sum(part.values())
            logger.debug("Part sum: %s", part_sum)
            rating_sum += part_sum

    logger.info("Part 1: %s", rating_sum)

    # part 2: ranges!

    import copy

    def split_for_comp(comp, in_range):
        left, outcome = comp
        if left is None:
            return in_range, outcome, None
        else:
            matched_outcome = copy.deepcopy(in_range)
            continue_outcome = copy.deepcopy(in_range)
            cat, op, val = left
            if op == "<":
                continue_outcome[cat][0] = val
                matched_outcome[cat][1] = val - 1
            elif op == ">":
                matched_outcome[cat][0] = val + 1
                continue_outcome[cat][1] = val
            if matched_outcome[cat][0] > matched_outcome[cat][1]:
                matched_outcome = None
            if continue_outcome[cat][0] > continue_outcome[cat][1]:
                continue_outcome = None
            return matched_outcome, outcome, continue_outcome

    continued = {c: [1, 4000] for c in "xmas"}
    workflow = "in"
    # return a list of ranges to outcomes
    matches = []
    queue = [(continued, workflow)]
    while queue:
        continued, workflow = queue.pop()
        logger.debug("Continued: %s", continued)
        logger.debug("Workflow: %s", workflow)
        for comp in rule_dict[workflow]:
            matched, outcome, continued = split_for_comp(comp, continued)
            if matched is not None:
                if outcome in "AR":
                    if outcome == "A":
                        matches.append(matched)
                else:
                    queue.append((matched, outcome))
        assert continued is None

    prod_ranges = 0
    for match in matches:
        prod = 1
        for cat, (low, high) in match.items():
            prod *= high - low + 1
        prod_ranges += prod
    logger.info("Part 2: %s", prod_ranges)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
