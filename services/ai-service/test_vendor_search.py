import io
import unittest
from contextlib import redirect_stdout

from vendor_search import (
    load_vendors,
    print_vendor_results,
    search_vendors,
    search_vendors_for_categories,
)


class VendorSearchTests(unittest.TestCase):

    def test_plastic_search_returns_all_vendors_with_same_location_first(self):
        vendors = search_vendors(
            category="plastics",
            business_location="Nasr City",
        )

        self.assertEqual(
            [vendor["name"] for vendor in vendors],
            [
                "Premium Plastic Buyers",
                "Green Plastic Recycling",
                "Maadi Plastic Buyers",
            ],
        )
        self.assertEqual(
            [vendor["same_location"] for vendor in vendors],
            [True, True, False],
        )
        self.assertEqual(
            [vendor["offer_price"] for vendor in vendors],
            [15, 12, 20],
        )

    def test_location_matching_is_case_insensitive_and_trimmed(self):
        vendors = search_vendors(
            category="plastics",
            business_location="  nasr city ",
        )

        self.assertTrue(all(vendor["same_location"] for vendor in vendors[:2]))
        self.assertFalse(vendors[-1]["same_location"])

    def test_search_without_location_ranks_by_offer_price(self):
        vendors = search_vendors(category="plastics")

        self.assertEqual(
            [vendor["name"] for vendor in vendors],
            [
                "Maadi Plastic Buyers",
                "Premium Plastic Buyers",
                "Green Plastic Recycling",
            ],
        )

    def test_search_returns_copies_with_pickup_data(self):
        vendors = search_vendors(
            category="plastics",
            business_location="Nasr City",
        )
        vendors[0]["name"] = "Changed locally"

        source_vendor = next(
            vendor
            for vendor in load_vendors()
            if vendor["id"] == vendors[0]["id"]
        )

        self.assertEqual(source_vendor["name"], "Premium Plastic Buyers")
        self.assertTrue(vendors[0]["pickup_available"])

    def test_multi_category_search_keeps_results_separate(self):
        results = search_vendors_for_categories(
            categories=["plastics", "paper_cardboard", "glass"],
            business_location="Nasr City",
        )

        self.assertEqual(
            list(results),
            ["plastics", "paper_cardboard", "glass"],
        )
        self.assertEqual(len(results["plastics"]), 3)
        self.assertEqual(
            [vendor["name"] for vendor in results["paper_cardboard"]],
            ["Cairo Paper Recycling"],
        )
        self.assertEqual(
            [vendor["name"] for vendor in results["glass"]],
            ["Glass Recycling Center"],
        )

    def test_single_category_output_includes_pickup_and_nearby_status(self):
        output = io.StringIO()

        with redirect_stdout(output):
            print_vendor_results(
                vendors=search_vendors(
                    category="plastics",
                    business_location="Nasr City",
                ),
                category="plastics",
                business_location="Nasr City",
            )

        rendered = output.getvalue()
        self.assertIn("Premium Plastic Buyers", rendered)
        self.assertIn("Pickup   : Available", rendered)
        self.assertIn("Nearby   : Yes", rendered)
        self.assertIn("Maadi Plastic Buyers", rendered)
        self.assertIn("Nearby   : No", rendered)


if __name__ == "__main__":
    unittest.main()
