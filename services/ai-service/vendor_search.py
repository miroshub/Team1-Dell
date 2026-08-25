import json
from pathlib import Path


# ============================================================
# 1. LOAD VENDORS
# ============================================================

VENDORS_FILE = Path(__file__).parent / "vendors.json"


def load_vendors():

    with open(
        VENDORS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# 2. SEARCH VENDORS FOR ONE CATEGORY
# ============================================================

def search_vendors(
    category,
    business_location=None
):

    vendors = load_vendors()

    matching_vendors = []

    for vendor in vendors:

        # ----------------------------------------------------
        # Check if vendor accepts this waste category
        # ----------------------------------------------------

        if category not in vendor["categories"]:
            continue

        # ----------------------------------------------------
        # Check location
        # ----------------------------------------------------

        same_location = False

        if business_location:

            same_location = (
                vendor["location"].strip().lower()
                == business_location.strip().lower()
            )

        # ----------------------------------------------------
        # Copy vendor
        # ----------------------------------------------------

        vendor_copy = vendor.copy()

        vendor_copy["same_location"] = same_location

        matching_vendors.append(vendor_copy)

    # ========================================================
    # SORT VENDORS
    # ========================================================
    #
    # Priority:
    #
    # 1. Same location first
    # 2. Higher offer price first
    #
    # IMPORTANT:
    # We DO NOT remove lower offers.
    #
    # Example:
    #
    # Premium Plastic Buyers -> 15 EGP/kg
    # Green Plastic Recycling -> 12 EGP/kg
    #
    # Both are returned.
    # ========================================================

    matching_vendors.sort(
        key=lambda vendor: (
            not vendor["same_location"],
            -vendor.get("offer_price", 0)
        )
    )

    return matching_vendors


# ============================================================
# 3. SEARCH VENDORS FOR MULTIPLE CATEGORIES
# ============================================================

def search_vendors_for_categories(
    categories,
    business_location=None
):

    results = {}

    for category in categories:

        results[category] = search_vendors(
            category=category,
            business_location=business_location
        )

    return results


# ============================================================
# 4. DISPLAY ONE CATEGORY
# ============================================================

def print_vendor_results(
    vendors,
    category,
    business_location
):

    print("\n" + "=" * 60)
    print("VENDOR RECOMMENDATION - CASE 1")
    print("=" * 60)

    print(
        f"\nDetected waste : {category}"
    )

    print(
        f"Business area  : {business_location}"
    )

    if not vendors:

        print(
            "\nNo vendors found "
            "for this waste category."
        )

        return

    print(
        f"\nFound {len(vendors)} "
        f"matching vendor(s):"
    )

    for index, vendor in enumerate(
        vendors,
        start=1
    ):

        print(
            f"\n{index}. "
            f"{vendor['name']}"
        )

        print(
            f"   Type     : "
            f"{vendor['vendor_type']}"
        )

        print(
            f"   Location : "
            f"{vendor['location']}"
        )

        print(
            f"   Offer    : "
            f"{vendor['offer_price']} "
            f"{vendor['price_unit']}"
        )

        print(
            f"   Pickup   : "
            f"{'Available' if vendor['pickup_available'] else 'Not available'}"
        )

        print(
            f"   Nearby   : "
            f"{'Yes' if vendor['same_location'] else 'No'}"
        )


# ============================================================
# 5. DISPLAY MULTIPLE CATEGORIES
# ============================================================

def print_multi_category_results(
    results,
    business_location
):

    print("\n" + "=" * 60)
    print("MULTI-CATEGORY VENDOR RECOMMENDATION - CASE 2")
    print("=" * 60)

    print(
        f"\nBusiness area: "
        f"{business_location}"
    )

    for category, vendors in results.items():

        print("\n" + "-" * 60)

        print(
            f"\nWaste category: "
            f"{category}"
        )

        if not vendors:

            print(
                "   No matching vendors found."
            )

            continue

        print(
            f"   Found {len(vendors)} "
            f"matching vendor(s):"
        )

        for index, vendor in enumerate(
            vendors,
            start=1
        ):

            print(
                f"\n   {index}. "
                f"{vendor['name']}"
            )

            print(
                f"      Type     : "
                f"{vendor['vendor_type']}"
            )

            print(
                f"      Location : "
                f"{vendor['location']}"
            )

            print(
                f"      Offer    : "
                f"{vendor['offer_price']} "
                f"{vendor['price_unit']}"
            )

            print(
                f"      Pickup   : "
                f"{'Available' if vendor['pickup_available'] else 'Not available'}"
            )

            print(
                f"      Nearby   : "
                f"{'Yes' if vendor['same_location'] else 'No'}"
            )


# ============================================================
# 6. TEST FEATURE 1
# ============================================================

if __name__ == "__main__":

    # ========================================================
    # MOCK BUSINESS DATA
    # ========================================================

    business_location = "Nasr City"


    # ========================================================
    # CHOOSE WHICH CASE TO TEST
    # ========================================================
    #
    # CASE 1 -> One waste category
    #
    # CASE 2 -> Multiple waste categories
    #
    # Change this number to switch between them.
    #
    # ========================================================

    TEST_CASE = 1


    # ========================================================
    # CASE 1
    # ========================================================
    #
    # Example:
    #
    # The image contains plastic bottles.
    #
    # Gemini's output would eventually be:
    #
    # "plastics"
    #
    # For now we MOCK that result.
    # ========================================================

    if TEST_CASE == 1:

        # Mock Gemini result
        detected_category = "plastics"

        # Search vendors
        results = search_vendors(
            category=detected_category,
            business_location=business_location
        )

        # Display results
        print_vendor_results(
            vendors=results,
            category=detected_category,
            business_location=business_location
        )


    # ========================================================
    # CASE 2
    # ========================================================
    #
    # Example:
    #
    # ONE image contains:
    #
    # Plastic bottle
    # Cardboard box
    # Glass bottle
    #
    # Gemini would eventually return:
    #
    # [
    #     "plastics",
    #     "paper_cardboard",
    #     "glass"
    # ]
    #
    # For now we MOCK that result.
    # ========================================================

    elif TEST_CASE == 2:

        # Mock Gemini result
        detected_categories = [
            "plastics",
            "paper_cardboard",
            "glass"
        ]

        # Search vendors for EVERY category
        results = search_vendors_for_categories(
            categories=detected_categories,
            business_location=business_location
        )

        # Display results
        print_multi_category_results(
            results=results,
            business_location=business_location
        )


    # ========================================================
    # INVALID TEST CASE
    # ========================================================

    else:

        print(
            "Invalid TEST_CASE."
        )

        print(
            "Use TEST_CASE = 1 or TEST_CASE = 2."
        )