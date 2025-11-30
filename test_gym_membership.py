"""
Unit tests for the Gym Membership Management System

Tests cover:
- Membership plan validation
- Additional features validation
- Number of members validation
- Base cost calculation
- Additional features cost calculation
- Group discount calculation
- Special offer discount calculation
- Premium surcharge calculation
- Total cost calculation with all discounts and surcharges
- Summary generation
"""

import unittest
from gym_membership import (
    GymMembershipManager,
    MembershipType,
    PremiumFeatureLevel,
    MembershipPlan,
    AdditionalFeature,
)


class TestMembershipValidation(unittest.TestCase):
    """Test membership plan validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def tearDown(self):
        """Clean up after tests"""
        # Reset availability flags
        for plan in self.manager.membership_plans.values():
            plan.available = True

    def test_validate_valid_membership_plan(self):
        """Test validation of valid membership plan"""
        is_valid, error_msg = self.manager.validate_membership_plan("Basic")
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)

    def test_validate_all_membership_plans(self):
        """Test validation of all available plans"""
        for plan_name in ["Basic", "Premium", "Family"]:
            is_valid, error_msg = self.manager.validate_membership_plan(plan_name)
            self.assertTrue(is_valid, f"Plan {plan_name} should be valid")
            self.assertIsNone(error_msg)

    def test_validate_invalid_membership_plan(self):
        """Test validation of non-existent membership plan"""
        is_valid, error_msg = self.manager.validate_membership_plan("InvalidPlan")
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg)

    def test_validate_unavailable_membership_plan(self):
        """Test validation when membership plan is unavailable"""
        self.manager.membership_plans["Basic"].available = False
        is_valid, error_msg = self.manager.validate_membership_plan("Basic")
        self.assertFalse(is_valid)
        self.assertIn("unavailable", error_msg)


class TestFeaturesValidation(unittest.TestCase):
    """Test additional features validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def tearDown(self):
        """Clean up after tests"""
        # Reset availability flags
        for feature in self.manager.additional_features.values():
            feature.available = True

    def test_validate_empty_features_list(self):
        """Test validation of empty features list"""
        is_valid, error_msg = self.manager.validate_features([])
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)

    def test_validate_valid_feature(self):
        """Test validation of valid feature"""
        is_valid, error_msg = self.manager.validate_features(["Personal Training"])
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)

    def test_validate_multiple_valid_features(self):
        """Test validation of multiple valid features"""
        is_valid, error_msg = self.manager.validate_features(
            ["Personal Training", "Group Classes"]
        )
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)

    def test_validate_invalid_feature(self):
        """Test validation of non-existent feature"""
        is_valid, error_msg = self.manager.validate_features(["InvalidFeature"])
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg)

    def test_validate_mixed_valid_invalid_features(self):
        """Test validation when mix of valid and invalid features"""
        is_valid, error_msg = self.manager.validate_features(
            ["Personal Training", "InvalidFeature"]
        )
        self.assertFalse(is_valid)

    def test_validate_unavailable_feature(self):
        """Test validation when feature is unavailable"""
        self.manager.additional_features["Personal Training"].available = False
        is_valid, error_msg = self.manager.validate_features(["Personal Training"])
        self.assertFalse(is_valid)
        self.assertIn("unavailable", error_msg)

    def test_validate_features_not_list(self):
        """Test validation when features not provided as list"""
        is_valid, error_msg = self.manager.validate_features("PersonalTraining")
        self.assertFalse(is_valid)
        self.assertIn("must be provided as a list", error_msg)


class TestNumMembersValidation(unittest.TestCase):
    """Test number of members validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_validate_single_member(self):
        """Test validation of single member"""
        is_valid, error_msg = self.manager.validate_num_members(1)
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)

    def test_validate_multiple_members(self):
        """Test validation of multiple members"""
        for num in [2, 5, 10]:
            is_valid, error_msg = self.manager.validate_num_members(num)
            self.assertTrue(is_valid, f"{num} members should be valid")

    def test_validate_zero_members(self):
        """Test validation of zero members"""
        is_valid, error_msg = self.manager.validate_num_members(0)
        self.assertFalse(is_valid)
        self.assertIn("at least 1", error_msg)

    def test_validate_negative_members(self):
        """Test validation of negative members"""
        is_valid, error_msg = self.manager.validate_num_members(-5)
        self.assertFalse(is_valid)

    def test_validate_too_many_members(self):
        """Test validation exceeding maximum"""
        is_valid, error_msg = self.manager.validate_num_members(11)
        self.assertFalse(is_valid)
        self.assertIn("cannot exceed 10", error_msg)

    def test_validate_non_integer_members(self):
        """Test validation with non-integer"""
        is_valid, error_msg = self.manager.validate_num_members(5.5)
        self.assertFalse(is_valid)
        self.assertIn("must be an integer", error_msg)


class TestCostCalculations(unittest.TestCase):
    """Test cost calculation functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_calculate_base_cost_basic(self):
        """Test base cost calculation for Basic plan"""
        cost = self.manager.calculate_base_cost("Basic")
        self.assertEqual(cost, 29.99)

    def test_calculate_base_cost_premium(self):
        """Test base cost calculation for Premium plan"""
        cost = self.manager.calculate_base_cost("Premium")
        self.assertEqual(cost, 59.99)

    def test_calculate_base_cost_family(self):
        """Test base cost calculation for Family plan"""
        cost = self.manager.calculate_base_cost("Family")
        self.assertEqual(cost, 99.99)

    def test_calculate_features_cost_empty(self):
        """Test features cost with no features"""
        cost = self.manager.calculate_features_cost([])
        self.assertEqual(cost, 0.0)

    def test_calculate_features_cost_single(self):
        """Test features cost with single feature"""
        cost = self.manager.calculate_features_cost(["Personal Training"])
        self.assertEqual(cost, 50.00)

    def test_calculate_features_cost_multiple(self):
        """Test features cost with multiple features"""
        cost = self.manager.calculate_features_cost(
            ["Personal Training", "Group Classes"]
        )
        self.assertEqual(cost, 80.00)

    def test_calculate_features_cost_all(self):
        """Test features cost with all features"""
        cost = self.manager.calculate_features_cost([
            "Personal Training",
            "Group Classes",
            "Nutritional Consulting"
        ])
        self.assertEqual(cost, 120.00)


class TestGroupDiscount(unittest.TestCase):
    """Test group discount calculation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_group_discount_single_member(self):
        """Test no discount for single member"""
        discounted, discount_amount = self.manager.calculate_group_discount(100.0, 1)
        self.assertEqual(discounted, 100.0)
        self.assertEqual(discount_amount, 0.0)

    def test_group_discount_two_members(self):
        """Test 10% discount for two members"""
        discounted, discount_amount = self.manager.calculate_group_discount(100.0, 2)
        self.assertEqual(discounted, 90.0)
        self.assertEqual(discount_amount, 10.0)

    def test_group_discount_five_members(self):
        """Test 10% discount for five members"""
        discounted, discount_amount = self.manager.calculate_group_discount(200.0, 5)
        self.assertEqual(discounted, 180.0)
        self.assertEqual(discount_amount, 20.0)

    def test_group_discount_calculation_precision(self):
        """Test discount calculation with decimal values"""
        discounted, discount_amount = self.manager.calculate_group_discount(99.99, 2)
        self.assertAlmostEqual(discount_amount, 9.999, places=2)
        self.assertAlmostEqual(discounted, 89.991, places=2)


class TestSpecialOfferDiscount(unittest.TestCase):
    """Test special offer discount calculation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_special_offer_no_discount_low_cost(self):
        """Test no discount for cost <= $200"""
        discounted, discount_amount = self.manager.calculate_special_offer_discount(100.0)
        self.assertEqual(discounted, 100.0)
        self.assertEqual(discount_amount, 0.0)

    def test_special_offer_discount_over_200(self):
        """Test $20 discount for cost > $200"""
        discounted, discount_amount = self.manager.calculate_special_offer_discount(250.0)
        self.assertEqual(discounted, 230.0)
        self.assertEqual(discount_amount, 20.0)

    def test_special_offer_discount_over_400(self):
        """Test $50 discount for cost > $400"""
        discounted, discount_amount = self.manager.calculate_special_offer_discount(450.0)
        self.assertEqual(discounted, 400.0)
        self.assertEqual(discount_amount, 50.0)

    def test_special_offer_boundary_200(self):
        """Test boundary case at exactly $200"""
        discounted, discount_amount = self.manager.calculate_special_offer_discount(200.0)
        self.assertEqual(discounted, 200.0)
        self.assertEqual(discount_amount, 0.0)

    def test_special_offer_boundary_200_01(self):
        """Test boundary case just over $200"""
        discounted, discount_amount = self.manager.calculate_special_offer_discount(200.01)
        self.assertEqual(discounted, 180.01)
        self.assertEqual(discount_amount, 20.0)

    def test_special_offer_boundary_400(self):
        """Test boundary case at exactly $400"""
        discounted, discount_amount = self.manager.calculate_special_offer_discount(400.0)
        # At exactly $400, should apply $20 discount (cost > 200 but NOT > 400)
        self.assertEqual(discounted, 380.0)
        self.assertEqual(discount_amount, 20.0)

    def test_special_offer_boundary_400_01(self):
        """Test boundary case just over $400"""
        discounted, discount_amount = self.manager.calculate_special_offer_discount(400.01)
        self.assertEqual(discounted, 350.01)
        self.assertEqual(discount_amount, 50.0)


class TestPremiumSurcharge(unittest.TestCase):
    """Test premium surcharge calculation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_premium_surcharge_none(self):
        """Test no surcharge for no premium level"""
        total, surcharge = self.manager.calculate_premium_surcharge(
            100.0,
            PremiumFeatureLevel.NONE
        )
        self.assertEqual(total, 100.0)
        self.assertEqual(surcharge, 0.0)

    def test_premium_surcharge_exclusive_facilities(self):
        """Test 15% surcharge for exclusive facilities"""
        total, surcharge = self.manager.calculate_premium_surcharge(
            100.0,
            PremiumFeatureLevel.EXCLUSIVE_FACILITIES
        )
        self.assertEqual(surcharge, 15.0)
        self.assertEqual(total, 115.0)

    def test_premium_surcharge_specialized_training(self):
        """Test 15% surcharge for specialized training"""
        total, surcharge = self.manager.calculate_premium_surcharge(
            200.0,
            PremiumFeatureLevel.SPECIALIZED_TRAINING
        )
        self.assertEqual(surcharge, 30.0)
        self.assertEqual(total, 230.0)

    def test_premium_surcharge_precision(self):
        """Test surcharge calculation with decimal values"""
        total, surcharge = self.manager.calculate_premium_surcharge(
            99.99,
            PremiumFeatureLevel.EXCLUSIVE_FACILITIES
        )
        self.assertAlmostEqual(surcharge, 14.9985, places=2)
        self.assertAlmostEqual(total, 114.9885, places=2)


class TestTotalCostCalculation(unittest.TestCase):
    """Test complete total cost calculation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_total_cost_basic_no_features(self):
        """Test total cost for basic plan with no features"""
        total, breakdown = self.manager.calculate_total_cost(
            "Basic", [], 1, PremiumFeatureLevel.NONE
        )
        self.assertEqual(breakdown['base_cost'], 29.99)
        self.assertEqual(breakdown['features_cost'], 0.0)
        self.assertEqual(breakdown['total_cost'], 29.99)
        self.assertEqual(int(total), 29)

    def test_total_cost_basic_with_features(self):
        """Test total cost for basic plan with features"""
        total, breakdown = self.manager.calculate_total_cost(
            "Basic",
            ["Personal Training"],
            1,
            PremiumFeatureLevel.NONE
        )
        self.assertEqual(breakdown['base_cost'], 29.99)
        self.assertEqual(breakdown['features_cost'], 50.00)
        self.assertEqual(breakdown['subtotal'], 79.99)
        self.assertEqual(breakdown['group_discount'], 0.0)
        self.assertAlmostEqual(breakdown['total_cost'], 79.99, places=2)

    def test_total_cost_with_group_discount(self):
        """Test total cost with group discount"""
        total, breakdown = self.manager.calculate_total_cost(
            "Basic", [], 2, PremiumFeatureLevel.NONE
        )
        self.assertAlmostEqual(breakdown['group_discount'], 2.999, places=2)
        self.assertAlmostEqual(breakdown['after_group_discount'], 26.991, places=2)

    def test_total_cost_with_group_discount_and_special_offer(self):
        """Test total cost with group and special offer discounts"""
        # Create a scenario where cost > 200 after group discount
        total, breakdown = self.manager.calculate_total_cost(
            "Family",  # Base: 99.99
            ["Personal Training", "Group Classes", "Nutritional Consulting"],  # Features: 120
            2,  # Group discount 10%
            PremiumFeatureLevel.NONE
        )
        # Subtotal: 219.99
        # After group discount (10%): 197.991
        # No special offer discount (not > 200)
        self.assertAlmostEqual(breakdown['special_offer_discount'], 0.0, places=2)

    def test_total_cost_with_special_offer_discount(self):
        """Test total cost with special offer discount"""
        total, breakdown = self.manager.calculate_total_cost(
            "Family",
            ["Personal Training", "Group Classes"],
            1,
            PremiumFeatureLevel.NONE
        )
        # Subtotal: 99.99 + 80 = 179.99
        # No special offer (not > 200)
        self.assertAlmostEqual(breakdown['special_offer_discount'], 0.0, places=2)

    def test_total_cost_with_premium_surcharge(self):
        """Test total cost with premium surcharge"""
        total, breakdown = self.manager.calculate_total_cost(
            "Premium",
            [],
            1,
            PremiumFeatureLevel.EXCLUSIVE_FACILITIES
        )
        # Base: 59.99
        # Surcharge: 59.99 * 0.15 = 8.9985
        self.assertGreater(breakdown['premium_surcharge'], 0.0)
        self.assertAlmostEqual(
            breakdown['total_cost'],
            breakdown['after_special_discount'] * 1.15,
            places=1
        )

    def test_total_cost_complex_scenario(self):
        """Test complex scenario with all discounts and surcharges"""
        total, breakdown = self.manager.calculate_total_cost(
            "Family",
            ["Personal Training", "Group Classes", "Nutritional Consulting"],
            2,
            PremiumFeatureLevel.EXCLUSIVE_FACILITIES
        )
        # Base: 99.99
        # Features: 120
        # Subtotal: 219.99
        # Group discount (10%): -21.999
        # After group: 197.991
        # No special offer yet
        # Premium surcharge: 197.991 * 0.15 ≈ 29.7
        # Total ≈ 227.7

        self.assertGreater(breakdown['group_discount'], 0.0)
        self.assertGreater(breakdown['premium_surcharge'], 0.0)
        self.assertGreater(breakdown['total_cost'], 220.0)
        self.assertLess(breakdown['total_cost'], 235.0)

    def test_total_cost_high_value_scenario(self):
        """Test high value scenario triggering $50 discount"""
        total, breakdown = self.manager.calculate_total_cost(
            "Family",
            ["Personal Training", "Group Classes", "Nutritional Consulting"],
            3,
            PremiumFeatureLevel.SPECIALIZED_TRAINING
        )
        # This should result in high cost triggering special offer discount
        self.assertGreater(breakdown['total_cost'], 200.0)

    def test_total_cost_integer_conversion(self):
        """Test that total cost can be converted to integer"""
        total, breakdown = self.manager.calculate_total_cost(
            "Basic",
            ["Personal Training"],
            1,
            PremiumFeatureLevel.NONE
        )
        integer_cost = int(total)
        self.assertIsInstance(integer_cost, int)
        self.assertEqual(integer_cost, int(79.99))


class TestSummaryGeneration(unittest.TestCase):
    """Test summary generation"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_summary_contains_plan_name(self):
        """Test summary contains membership plan name"""
        summary = self.manager.get_summary(
            "Basic", [], 1, PremiumFeatureLevel.NONE
        )
        self.assertIn("Basic", summary)

    def test_summary_contains_features(self):
        """Test summary contains selected features"""
        summary = self.manager.get_summary(
            "Basic",
            ["Personal Training"],
            1,
            PremiumFeatureLevel.NONE
        )
        self.assertIn("Personal Training", summary)

    def test_summary_contains_member_count(self):
        """Test summary contains number of members"""
        summary = self.manager.get_summary(
            "Basic", [], 3, PremiumFeatureLevel.NONE
        )
        self.assertIn("3", summary)

    def test_summary_contains_costs(self):
        """Test summary contains cost information"""
        summary = self.manager.get_summary(
            "Basic", [], 1, PremiumFeatureLevel.NONE
        )
        self.assertIn("29.99", summary)
        self.assertIn("TOTAL COST", summary)

    def test_summary_contains_discount_info(self):
        """Test summary contains discount information when applicable"""
        summary = self.manager.get_summary(
            "Basic", [], 2, PremiumFeatureLevel.NONE
        )
        self.assertIn("Group Discount", summary)

    def test_summary_contains_premium_info(self):
        """Test summary contains premium feature information"""
        summary = self.manager.get_summary(
            "Premium",
            [],
            1,
            PremiumFeatureLevel.EXCLUSIVE_FACILITIES
        )
        self.assertIn("Exclusive Facilities", summary)
        self.assertIn("Premium Surcharge", summary)

    def test_summary_formatting(self):
        """Test summary is properly formatted"""
        summary = self.manager.get_summary(
            "Family",
            ["Personal Training"],
            2,
            PremiumFeatureLevel.SPECIALIZED_TRAINING
        )
        # Check for section headers
        self.assertIn("MEMBERSHIP SUMMARY", summary)
        self.assertIn("COST BREAKDOWN", summary)
        # Check that it's not empty
        self.assertGreater(len(summary), 100)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_duplicate_features(self):
        """Test handling of duplicate features in list"""
        # Even if duplicates are in the list, cost should be calculated once per feature
        total, breakdown = self.manager.calculate_total_cost(
            "Basic",
            ["Personal Training", "Personal Training"],
            1,
            PremiumFeatureLevel.NONE
        )
        # Should calculate cost for both (feature list validation doesn't dedupe)
        self.assertEqual(breakdown['features_cost'], 100.0)

    def test_all_membership_plans_have_costs(self):
        """Test all membership plans have valid costs"""
        for plan_name in ["Basic", "Premium", "Family"]:
            cost = self.manager.calculate_base_cost(plan_name)
            self.assertGreater(cost, 0)
            self.assertIsInstance(cost, float)

    def test_all_features_have_costs(self):
        """Test all features have valid costs"""
        for feature_name in [
            "Personal Training",
            "Group Classes",
            "Nutritional Consulting"
        ]:
            feature = self.manager.additional_features[feature_name]
            self.assertGreater(feature.cost, 0)
            self.assertIsInstance(feature.cost, float)

    def test_zero_cost_input(self):
        """Test calculations with zero cost"""
        discounted, discount = self.manager.calculate_group_discount(0.0, 2)
        self.assertEqual(discounted, 0.0)
        self.assertEqual(discount, 0.0)

    def test_very_large_cost(self):
        """Test calculations with very large costs"""
        total, breakdown = self.manager.calculate_total_cost(
            "Family",
            ["Personal Training", "Group Classes", "Nutritional Consulting"],
            10,
            PremiumFeatureLevel.SPECIALIZED_TRAINING
        )
        # Should not crash and should be positive
        self.assertGreater(breakdown['total_cost'], 0)
        self.assertLess(breakdown['total_cost'], 10000)  # Sanity check


class TestPlanSelection(unittest.TestCase):
    """Test membership plan selection and availability"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_get_available_plans(self):
        """Test getting available membership plans"""
        plans = self.manager.get_available_membership_plans()
        self.assertEqual(len(plans), 3)

    def test_get_available_features(self):
        """Test getting available additional features"""
        features = self.manager.get_available_features()
        self.assertEqual(len(features), 3)

    def test_plan_count_matches_enum_count(self):
        """Test that number of plans is reasonable"""
        plans = self.manager.get_available_membership_plans()
        self.assertEqual(len(plans), 3)

    def test_feature_count_matches_enum_count(self):
        """Test that number of features is reasonable"""
        features = self.manager.get_available_features()
        self.assertEqual(len(features), 3)


class TestCalculationOrder(unittest.TestCase):
    """Test that discounts and surcharges are applied in correct order"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = GymMembershipManager()

    def test_discount_order_group_then_special(self):
        """
        Test that group discount is applied before special offer discount
        """
        # Base: 99.99, Features: 120 = 219.99
        # After group (10%): 197.991
        # Special offer should NOT apply (197.991 < 200)
        total, breakdown = self.manager.calculate_total_cost(
            "Family",
            ["Personal Training", "Group Classes"],
            2,
            PremiumFeatureLevel.NONE
        )
        # Group discount should be applied
        self.assertGreater(breakdown['group_discount'], 0)
        # But special offer should not (cost after group is < 200)
        self.assertEqual(breakdown['special_offer_discount'], 0)

    def test_surcharge_order_applied_last(self):
        """
        Test that premium surcharge is applied AFTER all other discounts
        """
        # This ensures the surcharge is 15% of the discounted amount
        total, breakdown = self.manager.calculate_total_cost(
            "Basic",
            ["Personal Training"],
            2,
            PremiumFeatureLevel.EXCLUSIVE_FACILITIES
        )
        # Base: 29.99, Features: 50 = 79.99
        # After group (10%): 71.991
        # Premium surcharge: 71.991 * 0.15 ≈ 10.8
        # Total ≈ 82.8

        self.assertGreater(breakdown['premium_surcharge'], 0)
        # Verify surcharge is applied to post-discount amount
        surcharge_percentage = (
            breakdown['premium_surcharge'] / breakdown['after_special_discount']
        )
        self.assertAlmostEqual(surcharge_percentage, 0.15, places=1)


def run_tests():
    """Run all tests with detailed output"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMembershipValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestFeaturesValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestNumMembersValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestCostCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestGroupDiscount))
    suite.addTests(loader.loadTestsFromTestCase(TestSpecialOfferDiscount))
    suite.addTests(loader.loadTestsFromTestCase(TestPremiumSurcharge))
    suite.addTests(loader.loadTestsFromTestCase(TestTotalCostCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestSummaryGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPlanSelection))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculationOrder))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    result = run_tests()
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
