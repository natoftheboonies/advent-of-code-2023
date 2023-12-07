"""
Author: Nat with Darren's Template
Date: 2023-12-07

Solving https://adventofcode.com/2023/day/1

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2023
DAY = 7

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

card_types = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
card_types.reverse()


def score(hand):
    cards = list(hand)
    unique_cards = set(cards)
    if len(unique_cards) == 5:
        return 0
    if len(unique_cards) == 4:
        # one pair
        return 1
    if len(unique_cards) == 3:
        # two pair or three of a kind
        three_of_a_kind = False
        for card in unique_cards:
            if cards.count(card) == 3:
                three_of_a_kind = True
                break
        if three_of_a_kind:
            return 3
        # else two pair
        return 2
    if len(unique_cards) == 2:
        # full house or four of a kind
        four_of_a_kind = False
        for card in unique_cards:
            if cards.count(card) == 4:
                four_of_a_kind = True
                break
        if four_of_a_kind:
            return 5
        return 4
    else:
        assert len(unique_cards) == 1
        # five of a kind
        return 6


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    logger.debug(data)
    sort_me = []
    for hand in data:
        cards, wager = hand.split()
        wager = int(wager)
        card_values = [card_types.index(card) for card in cards]
        sort_me.append((score(cards), *card_values, cards, wager))
    sort_me.sort()
    logger.debug(sort_me)
    product = 0
    for i, hand in enumerate(sort_me):
        logger.debug(hand)
        product += hand[-1] * (i + 1)
    logger.info("Part 1: %d", product)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
