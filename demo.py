#!/usr/bin/env python3
"""
Example demonstrations of the Gym Membership Management System

Shows various scenarios and calculates costs for different membership configurations.
"""

from gym_membership import GymMembershipManager, PremiumFeatureLevel


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70 + "\n")


def demonstrate_basic_scenarios():
    """Demonstrate basic membership scenarios"""
    print_section("BASIC SCENARIOS")
    
    manager = GymMembershipManager()
    
    # Scenario 1: Single member, basic plan, no features
    print("Scenario 1: Single Member - Basic Plan")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Basic", [], 1, PremiumFeatureLevel.NONE
    )
    print(manager.get_summary("Basic", [], 1, PremiumFeatureLevel.NONE))
    
    # Scenario 2: Single member, premium plan
    print("Scenario 2: Single Member - Premium Plan")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Premium", [], 1, PremiumFeatureLevel.NONE
    )
    print(manager.get_summary("Premium", [], 1, PremiumFeatureLevel.NONE))
    
    # Scenario 3: Single member, family plan
    print("Scenario 3: Single Member - Family Plan")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Family", [], 1, PremiumFeatureLevel.NONE
    )
    print(manager.get_summary("Family", [], 1, PremiumFeatureLevel.NONE))


def demonstrate_features_scenarios():
    """Demonstrate scenarios with additional features"""
    print_section("SCENARIOS WITH ADDITIONAL FEATURES")
    
    manager = GymMembershipManager()
    
    # Scenario 1: With personal training
    print("Scenario 1: Premium Plan + Personal Training")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Premium", 
        ["Personal Training"], 
        1, 
        PremiumFeatureLevel.NONE
    )
    print(manager.get_summary(
        "Premium", 
        ["Personal Training"], 
        1, 
        PremiumFeatureLevel.NONE
    ))
    
    # Scenario 2: With multiple features
    print("Scenario 2: Premium Plan + Multiple Features")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Premium",
        ["Personal Training", "Group Classes"],
        1,
        PremiumFeatureLevel.NONE
    )
    print(manager.get_summary(
        "Premium",
        ["Personal Training", "Group Classes"],
        1,
        PremiumFeatureLevel.NONE
    ))
    
    # Scenario 3: All features
    print("Scenario 3: Family Plan + All Features")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Family",
        ["Personal Training", "Group Classes", "Nutritional Consulting"],
        1,
        PremiumFeatureLevel.NONE
    )
    print(manager.get_summary(
        "Family",
        ["Personal Training", "Group Classes", "Nutritional Consulting"],
        1,
        PremiumFeatureLevel.NONE
    ))


def demonstrate_group_discounts():
    """Demonstrate group discount scenarios"""
    print_section("GROUP DISCOUNT SCENARIOS")
    
    manager = GymMembershipManager()
    
    # Scenario 1: 2 members
    print("Scenario 1: 2 Members - Basic Plan (10% Group Discount)")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Basic", [], 2, PremiumFeatureLevel.NONE
    )
    print(manager.get_summary("Basic", [], 2, PremiumFeatureLevel.NONE))
    
    # Scenario 2: 3 members with features
    print("Scenario 2: 3 Members - Premium Plan + Features")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Premium",
        ["Personal Training", "Group Classes"],
        3,
        PremiumFeatureLevel.NONE
    )
    print(manager.get_summary(
        "Premium",
        ["Personal Training", "Group Classes"],
        3,
        PremiumFeatureLevel.NONE
    ))
    
    # Scenario 3: 5 members, family plan
    print("Scenario 3: 5 Members - Family Plan")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Family", [], 5, PremiumFeatureLevel.NONE
    )
    print(manager.get_summary("Family", [], 5, PremiumFeatureLevel.NONE))


def demonstrate_special_offers():
    """Demonstrate special offer discount scenarios"""
    print_section("SPECIAL OFFER DISCOUNT SCENARIOS")
    
    manager = GymMembershipManager()
    
    # Scenario 1: Total > $200, gets $20 discount
    print("Scenario 1: Family + 1 Feature (Total ~$150, No Special Discount)")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Family",
        ["Personal Training"],
        1,
        PremiumFeatureLevel.NONE
    )
    print(manager.get_summary(
        "Family",
        ["Personal Training"],
        1,
        PremiumFeatureLevel.NONE
    ))
    
    # Scenario 2: Total > $200, gets $20 discount
    print("Scenario 2: Family + All Features (Total ~$220, Gets $20 Discount)")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Family",
        ["Personal Training", "Group Classes", "Nutritional Consulting"],
        1,
        PremiumFeatureLevel.NONE
    )
    print(manager.get_summary(
        "Family",
        ["Personal Training", "Group Classes", "Nutritional Consulting"],
        1,
        PremiumFeatureLevel.NONE
    ))


def demonstrate_premium_features():
    """Demonstrate premium feature scenarios"""
    print_section("PREMIUM FEATURE SCENARIOS")
    
    manager = GymMembershipManager()
    
    # Scenario 1: Exclusive facilities
    print("Scenario 1: Premium Plan + Exclusive Facilities (15% Surcharge)")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Premium",
        [],
        1,
        PremiumFeatureLevel.EXCLUSIVE_FACILITIES
    )
    print(manager.get_summary(
        "Premium",
        [],
        1,
        PremiumFeatureLevel.EXCLUSIVE_FACILITIES
    ))
    
    # Scenario 2: Specialized training with features
    print("Scenario 2: Family + Features + Specialized Training")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Family",
        ["Personal Training", "Group Classes"],
        1,
        PremiumFeatureLevel.SPECIALIZED_TRAINING
    )
    print(manager.get_summary(
        "Family",
        ["Personal Training", "Group Classes"],
        1,
        PremiumFeatureLevel.SPECIALIZED_TRAINING
    ))


def demonstrate_complex_scenarios():
    """Demonstrate complex scenarios with multiple factors"""
    print_section("COMPLEX SCENARIOS - ALL FACTORS COMBINED")
    
    manager = GymMembershipManager()
    
    # Scenario 1: Complex with all discounts and surcharges
    print("Scenario 1: 2 Members - Family + All Features + Premium")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Family",
        ["Personal Training", "Group Classes", "Nutritional Consulting"],
        2,
        PremiumFeatureLevel.EXCLUSIVE_FACILITIES
    )
    print(manager.get_summary(
        "Family",
        ["Personal Training", "Group Classes", "Nutritional Consulting"],
        2,
        PremiumFeatureLevel.EXCLUSIVE_FACILITIES
    ))
    print(f"Final Cost as Integer: {int(total)}\n")
    
    # Scenario 2: Another complex scenario
    print("Scenario 2: 3 Members - Premium + 2 Features + Specialized Training")
    print("-" * 70)
    total, breakdown = manager.calculate_total_cost(
        "Premium",
        ["Personal Training", "Nutritional Consulting"],
        3,
        PremiumFeatureLevel.SPECIALIZED_TRAINING
    )
    print(manager.get_summary(
        "Premium",
        ["Personal Training", "Nutritional Consulting"],
        3,
        PremiumFeatureLevel.SPECIALIZED_TRAINING
    ))
    print(f"Final Cost as Integer: {int(total)}\n")


def demonstrate_validation():
    """Demonstrate validation features"""
    print_section("VALIDATION EXAMPLES")
    
    manager = GymMembershipManager()
    
    print("1. Valid Plan - 'Premium':")
    is_valid, msg = manager.validate_membership_plan("Premium")
    print(f"   Valid: {is_valid}, Message: {msg}\n")
    
    print("2. Invalid Plan - 'InvalidPlan':")
    is_valid, msg = manager.validate_membership_plan("InvalidPlan")
    print(f"   Valid: {is_valid}, Message: {msg}\n")
    
    print("3. Valid Features - ['Personal Training', 'Group Classes']:")
    is_valid, msg = manager.validate_features(["Personal Training", "Group Classes"])
    print(f"   Valid: {is_valid}, Message: {msg}\n")
    
    print("4. Invalid Features - ['InvalidFeature']:")
    is_valid, msg = manager.validate_features(["InvalidFeature"])
    print(f"   Valid: {is_valid}, Message: {msg}\n")
    
    print("5. Valid Members - 3:")
    is_valid, msg = manager.validate_num_members(3)
    print(f"   Valid: {is_valid}, Message: {msg}\n")
    
    print("6. Invalid Members - 15:")
    is_valid, msg = manager.validate_num_members(15)
    print(f"   Valid: {is_valid}, Message: {msg}\n")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("GYM MEMBERSHIP MANAGEMENT SYSTEM - DEMONSTRATION".center(70))
    print("=" * 70)
    
    demonstrate_basic_scenarios()
    demonstrate_features_scenarios()
    demonstrate_group_discounts()
    demonstrate_special_offers()
    demonstrate_premium_features()
    demonstrate_complex_scenarios()
    demonstrate_validation()
    
    print_section("DEMONSTRATION COMPLETE")
    print("For interactive mode, run: python gym_membership.py")
    print("For unit tests, run:       python test_gym_membership.py\n")


if __name__ == "__main__":
    main()
