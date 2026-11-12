"""Tests for the regression data generator (bonus, option A).

What is tested here is that the generator produces valid orders, that it is
reproducible, and that the file it writes can be read back. The amounts are
not asserted: they come from the calculator itself, so checking them would be
comparing the code against itself. That check lives in
test_order_calculator.py, against values written by hand.
"""

import csv
import json

import pytest

from data_generator import HEADER, generate_orders, main, write_csv
from order_calculator import Order

ORDERS = generate_orders(100)


class TestGeneration:
    """Count, shape and validity of what is generated."""

    def test_it_generates_the_hundred_orders_the_brief_asks_for(self):
        assert len(ORDERS) == 100

    def test_the_names_do_not_repeat(self):
        names = [order["test_name"] for order in ORDERS]
        assert len(set(names)) == len(names)

    def test_every_order_is_accepted_by_the_calculator(self):
        """No generated order may make the constructor fail."""
        for order in ORDERS:
            Order(order["items"], order["customer_type"])

    def test_every_order_has_at_least_one_article(self):
        assert all(order["items"] for order in ORDERS)

    def test_the_articles_carry_the_four_fields(self):
        for order in ORDERS:
            for item in order["items"]:
                assert set(item) == {"name", "price", "quantity", "weight"}

    def test_it_generates_no_negative_values(self):
        for order in ORDERS:
            assert order["distance_km"] >= 0
            for item in order["items"]:
                assert item["price"] >= 0 and item["quantity"] >= 0 and item["weight"] >= 0

    def test_the_breakdown_comes_complete(self):
        for order in ORDERS:
            assert set(order["expected"]) == {"subtotal", "discount", "tax", "shipping", "total"}

    def test_the_variety_covers_discounts_and_express(self):
        """A generator that always produces the same thing is no regression set."""
        codes = {order["discount_code"] for order in ORDERS}
        assert len(codes) >= 4
        assert {order["is_express"] for order in ORDERS} == {True, False}
        assert {order["customer_type"] for order in ORDERS} == {"regular", "new"}


class TestReproducibility:
    """The same seed has to produce the same file."""

    def test_the_same_seed_gives_the_same_thing(self):
        assert generate_orders(10, seed=7) == generate_orders(10, seed=7)

    def test_different_seeds_give_different_things(self):
        assert generate_orders(10, seed=7) != generate_orders(10, seed=8)

    @pytest.mark.parametrize("count", [0, -1, 1.5, "hundred", None, True])
    def test_an_invalid_count(self, count):
        with pytest.raises(ValueError, match="count must be a positive integer"):
            generate_orders(count)


class TestTheFile:
    """The CSV that gets written has to be readable again."""

    def test_the_header_and_the_rows_line_up(self, tmp_path):
        path = write_csv(generate_orders(5), str(tmp_path / "gen.csv"))

        with open(path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        assert len(rows) == 5
        assert tuple(rows[0]) == HEADER

    def test_the_items_read_back_as_json(self, tmp_path):
        path = write_csv(generate_orders(5), str(tmp_path / "gen.csv"))

        with open(path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                assert isinstance(json.loads(row["items"]), list)

    def test_the_amounts_keep_two_decimals(self, tmp_path):
        path = write_csv(generate_orders(5), str(tmp_path / "gen.csv"))

        with open(path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for column in ("expected_subtotal", "expected_total"):
                    assert len(row[column].split(".")[1]) == 2


def test_main_writes_the_file(tmp_path):
    """main() is the entry point run by hand to regenerate the set."""
    path = main(str(tmp_path / "regression.csv"), count=3)

    with open(path, newline="", encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 3
