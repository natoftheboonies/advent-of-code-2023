"""
Author: Nat with Darren's Template
Date: 2023-12-20

Solving https://adventofcode.com/2023/day/20

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac
from collections import deque

YEAR = 2023
DAY = 20

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def run_queue(button_press, modules):
    low_pulses = 0
    high_pulses = 0
    queue = deque([button_press])  # (module, signal, source)
    logger.debug(f"{queue}")
    while queue:
        name, signal, source = queue.popleft()
        # TODO ai below
        logger.debug(f"queue: {source} -{'high' if signal else 'low'}-> {name}")
        if signal == 0:
            low_pulses += 1
        else:
            assert signal == 1
            high_pulses += 1
        module = modules[name]
        if module["type"] == "broadcast":
            # broadcast to all
            for notify in module["notify"]:
                queue.append((notify, signal, name))
        elif module["type"] == "%":
            # flip-flop ignores high pulses
            if signal == 1:
                continue
            # otherwise flip and notify
            module["state"] += 1
            module["state"] %= 2
            for notify in module["notify"]:
                queue.append((notify, module["state"], name))
        elif module["type"] == "&":
            # remember last pulse for each input
            assert source in module["received"]
            module["received"][source] = signal
            send = 1
            if all(sig == 1 for sig in module["received"].values()):
                # all inputs are high
                send = 0
            for notify in module["notify"]:
                queue.append((notify, send, name))
        elif module["type"] is None:
            continue
        else:
            assert False
    return low_pulses, high_pulses


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    modules = {}
    all_notify = set()
    for line in data:
        left, right = line.split(" -> ")
        # logger.debug(f"{left} -> {right}")
        if "," in right:
            right = right.split(", ")

        if left[0] == "%":
            name = left[1:]
            state = 0
            notify = right if isinstance(right, list) else [right]
            modules[name] = {"type": "%", "state": state, "notify": notify}
        elif left[0] == "&":
            name = left[1:]
            received = {}
            notify = right if isinstance(right, list) else [right]
            modules[name] = {"type": "&", "received": received, "notify": notify}
        else:
            assert left == "broadcaster"
            name = left
            modules[left] = {"type": "broadcast", "notify": right}
        all_notify.update(modules[name]["notify"])

    # add untyped
    for name in all_notify:
        logger.debug(f"{name}")
        if name not in modules:
            modules[name] = {"type": None, "notify": []}

    for name, module in modules.items():
        for notify in module["notify"]:
            if modules[notify]["type"] == "&":
                modules[notify]["received"][name] = 0
    # fi
    for module in modules.values():
        logger.debug(f"{module}")
    # button sends to broadcaster
    low_pulses = 0
    high_pulses = 0
    button_press = ("broadcaster", 0, "button")
    for _ in range(1000):
        low, high = run_queue(button_press, modules)
        low_pulses += low
        high_pulses += high
    logger.info(f"low pulses: {low_pulses}")
    logger.info(f"high pulses: {high_pulses}")
    logger.info("Part 1: %d", low_pulses * high_pulses)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
