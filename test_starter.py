import unittest
from decimal import Decimal

from starter import recommend_price


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    async def test_applies_discount_to_cheapest_eligible_competitor(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "MyShOp", "price": Decimal("4300.00"), "delivery_days": 2},
                    {"seller": "UNKNOWN", "price": Decimal("4400.00"), "delivery_days": None},
                    {"seller": "SLOW", "price": Decimal("4700.00"), "delivery_days": 7},
                    {"seller": "OTHER", "price": Decimal("4850.00"), "delivery_days": 2},
                    {"seller": "PARTS", "price": Decimal("4800.01"), "delivery_days": 6},
                ],
            }

        result = await recommend_price(fetch_offers, Decimal("4900.00"), Decimal("4500.00"))

        self.assertIsInstance(result["price"], Decimal)
        self.assertEqual(result["price"], Decimal("4728.00"))
        self.assertEqual(result["decision"], "APPLY")

    async def test_applies_minimum_price_at_exactly_thirty_percent_increase(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "PARTS", "price": Decimal("120.00"), "delivery_days": 1},
                ],
            }

        result = await recommend_price(fetch_offers, Decimal("100.00"), Decimal("130.00"))

        self.assertEqual(result["price"], Decimal("130.00"))
        self.assertEqual(result["decision"], "APPLY")
