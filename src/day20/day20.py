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
from math import lcm

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
    queue = deque([button_press])  # (name, signal, source)
    signals = []
    while queue:
        name, signal, source = queue.popleft()
        signals.append((name, signal))
        # logger.debug(f"queue: {source} -{'high' if signal else 'low'}-> {name}")
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
    return signals


def parse_modules(data):
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
        if name not in modules:
            modules[name] = {"type": None, "notify": []}

    for name, module in modules.items():
        for notify in module["notify"]:
            if modules[notify]["type"] == "&":
                modules[notify]["received"][name] = 0
    return modules


def part1(data):
    modules = parse_modules(data)
    low_pulses = 0
    high_pulses = 0
    button_press = ("broadcaster", 0, "button")
    for _ in range(1000):
        signals = run_queue(button_press, modules)
        low_pulses += sum(1 for _, x in signals if x == 0)
        high_pulses += sum(1 for _, x in signals if x == 1)
    logger.debug(f"low pulses: {low_pulses}")
    logger.debug(f"high pulses: {high_pulses}")
    logger.info("Part 1: %d", low_pulses * high_pulses)


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    part1(data)

    # part 2: when does rx receive 1?
    # rx comes from &bb fed by 4 &s
    modules = parse_modules(data)
    princess = "rx"
    final_boss = [
        name for name, module in modules.items() if princess in module["notify"]
    ]
    assert len(final_boss) == 1
    final_boss = final_boss[0]
    logger.debug("boss: %s", final_boss)
    # final boss sends 0 when all minions send 1
    # minions send 1 when they receive 0
    # they receive 0 in the middle of a button press...
    minions = {
        name: 0 for name, module in modules.items() if final_boss in module["notify"]
    }

    button_press = ("broadcaster", 0, "button")
    i = 1
    while not all(minions.values()):
        signals = run_queue(button_press, modules)
        for name, signal in signals:
            if name in minions and signal == 0:
                minions[name] = i
                logger.debug("minion %s: %d", name, i)
        i += 1

    logger.info("Part 2: %d", lcm(*minions.values()))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
