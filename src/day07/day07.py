"""
Author: Nat with Darren's Template
Date: 2023-12-07

Solving https://adventofcode.com/2023/day/7

Part 1: Sort poker-ish hands

Part 2: Jokers are wild

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

part_two_types = card_types.copy()
part_two_types.remove("J")
part_two_types.insert(0, "J")


# collections.Counter does this a lot more efficiently :)
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


def upgrade(hand):
    cards = list(hand)
    unique_cards = set(cards)
    if "J" not in unique_cards:
        return hand
    if len(unique_cards) == 5:
        # make a pair
        scores = [part_two_types.index(card) for card in cards]
        max_score = max(scores)
        pair_card = cards[scores.index(max_score)]
        logger.debug("pair_card: %s", pair_card)
        return hand.replace("J", pair_card)
    if len(unique_cards) == 4:
        # one pair, if pair is J, upgrade to highest other card
        if cards.count("J") == 2:
            scores = [part_two_types.index(card) for card in cards]
            max_score = max(scores)
            pair_card = cards[scores.index(max_score)]
            return hand.replace("J", pair_card)
        # upgrade to three of a kind
        pair_card = None
        for card in unique_cards:
            if cards.count(card) == 2:
                pair_card = card
                break
        assert pair_card is not None
        return hand.replace("J", pair_card)
    if len(unique_cards) == 3:
        # two pair or three of a kind
        three_of_a_kind = False
        three_card = None
        for card in unique_cards:
            if cards.count(card) == 3:
                three_of_a_kind = True
                three_card = card
                break
        if three_of_a_kind:
            # if three card is J, upgrade to max other card
            if three_card == "J":
                scores = [part_two_types.index(card) for card in cards]
                max_score = max(scores)
                other_card = cards[scores.index(max_score)]
                return hand.replace("J", other_card)
            return hand.replace("J", three_card)
        # else two pair
        pair_cards = []
        for card in unique_cards:
            if cards.count(card) == 2:
                pair_cards.append(card)
        assert len(pair_cards) == 2
        if "J" in pair_cards:
            pair_cards.remove("J")
            # make 4 of a kind
            return hand.replace("J", pair_cards[0])
        pair_cards.sort()
        # make full house
        return hand.replace("J", pair_cards[1])
    if len(unique_cards) == 2:
        # full house or four of a kind
        four_of_a_kind = False
        four_card = None
        for card in unique_cards:
            if cards.count(card) == 4:
                four_of_a_kind = True
                four_card = card
                break
        if four_of_a_kind:
            # if four card is J, upgrade to other card
            if four_card == "J":
                other_card = None
                for card in unique_cards:
                    if card != "J":
                        other_card = card
                        break
                return hand.replace("J", other_card)
            return hand.replace("J", four_card)
        # else full house, upgrade to 5 of a kind
        three_card = None
        two_card = None
        for card in unique_cards:
            if cards.count(card) == 3:
                three_card = card
            else:
                two_card = card
        assert three_card is not None and two_card is not None
        if three_card == "J":
            return hand.replace("J", two_card)
        return hand.replace("J", three_card)

    return hand


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

    # Part 2
    sort_me = []
    for hand in data:
        # logger.debug(hand)
        cards, wager = hand.split()
        wager = int(wager)
        upgraded = upgrade(cards)
        if upgraded != cards:
            logger.debug("upgraded %s to %s", cards, upgraded)
        card_values = [part_two_types.index(card) for card in cards]
        sort_me.append((score(upgraded), *card_values, cards, upgraded, wager))
    sort_me.sort()
    # logger.debug(sort_me)
    product = 0
    for i, hand in enumerate(sort_me):
        # logger.debug(hand)
        product += hand[-1] * (i + 1)
    logger.info("Part 2: %d", product)
    # 253091321 too low
    # 253221750 too low
    # 253372014 too low


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
