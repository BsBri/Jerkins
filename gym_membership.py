"""
Gym Membership Management System

This system manages gym memberships with:
- Multiple membership plans (Basic, Premium, Family)
- Additional features per membership
- Cost calculation with base + features
- Group discounts (10% for 2+ members)
- Special offer discounts ($20 if >$200, $50 if >$400)
- Premium membership surcharge (15%)
- User confirmation workflow

Assumptions:
1. All costs are in USD
2. Discounts are applied in order: group discount -> special offer discount -> premium surcharge
3. Final cost is returned as a positive integer or -1 for invalid/canceled
4. Premium surcharge is applied AFTER all other discounts
5. Group size >= 2 triggers the 10% discount
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class MembershipType(Enum):
    """Available gym membership plans"""
    BASIC = "Basic"
    PREMIUM = "Premium"
    FAMILY = "Family"


class PremiumFeatureLevel(Enum):
    """Premium feature levels that trigger surcharge"""
    NONE = "None"
    EXCLUSIVE_FACILITIES = "Exclusive Facilities"
    SPECIALIZED_TRAINING = "Specialized Training"


@dataclass
class MembershipPlan:
    """Represents a gym membership plan"""
    name: str
    base_cost: float
    benefits: List[str]
    available: bool = True

    def __repr__(self) -> str:
        benefits_str = ", ".join(self.benefits)
        return f"{self.name} (${self.base_cost:.2f}) - Benefits: {benefits_str}"


@dataclass
class AdditionalFeature:
    """Represents an additional feature that can be added to a membership"""
    name: str
    cost: float
    available: bool = True

    def __repr__(self) -> str:
        return f"{self.name} (${self.cost:.2f})"


@dataclass
class MembershipSelection:
    """Represents a user's membership selection"""
    plan: MembershipPlan
    additional_features: List[AdditionalFeature]
    premium_feature_level: PremiumFeatureLevel
    num_members: int = 1

    def __repr__(self) -> str:
        return (
            f"Membership: {self.plan.name}, "
            f"Features: {[f.name for f in self.additional_features]}, "
            f"Members: {self.num_members}, "
            f"Premium Level: {self.premium_feature_level.value}"
        )


class GymMembershipManager:
    """Manages gym membership selection and cost calculation"""

    # Predefined membership plans
    MEMBERSHIP_PLANS: Dict[str, MembershipPlan] = {
        "Basic": MembershipPlan(
            name="Basic",
            base_cost=29.99,
            benefits=["Access to gym equipment", "Basic locker room access"],
            available=True
        ),
        "Premium": MembershipPlan(
            name="Premium",
            base_cost=59.99,
            benefits=["Access to gym equipment", "Premium locker room", "Sauna access"],
            available=True
        ),
        "Family": MembershipPlan(
            name="Family",
            base_cost=99.99,
            benefits=["Up to 4 family members", "All Premium benefits", "Family lounge access"],
            available=True
        ),
    }

    # Predefined additional features
    ADDITIONAL_FEATURES: Dict[str, AdditionalFeature] = {
        "Personal Training": AdditionalFeature(
            name="Personal Training",
            cost=50.00,
            available=True
        ),
        "Group Classes": AdditionalFeature(
            name="Group Classes",
            cost=30.00,
            available=True
        ),
        "Nutritional Consulting": AdditionalFeature(
            name="Nutritional Consulting",
            cost=40.00,
            available=True
        ),
    }

    # Special offer discount thresholds
    SPECIAL_OFFER_DISCOUNTS = [
        (200, 20),    # $20 discount if cost > $200
        (400, 50),    # $50 discount if cost > $400
    ]

    # Group discount
    GROUP_DISCOUNT_THRESHOLD = 2
    GROUP_DISCOUNT_PERCENTAGE = 0.10

    # Premium surcharge
    PREMIUM_SURCHARGE_PERCENTAGE = 0.15

    def __init__(self):
        """Initialize the membership manager"""
        self.membership_plans = self.MEMBERSHIP_PLANS.copy()
        self.additional_features = self.ADDITIONAL_FEATURES.copy()

    def get_available_membership_plans(self) -> List[MembershipPlan]:
        """Return list of available membership plans"""
        return [plan for plan in self.membership_plans.values() if plan.available]

    def get_available_features(self) -> List[AdditionalFeature]:
        """Return list of available additional features"""
        return [feature for feature in self.additional_features.values() if feature.available]

    def validate_membership_plan(self, plan_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if membership plan exists and is available
        
        Returns: (is_valid, error_message)
        """
        if plan_name not in self.membership_plans:
            return False, f"Membership plan '{plan_name}' does not exist."

        if not self.membership_plans[plan_name].available:
            return False, f"Membership plan '{plan_name}' is currently unavailable."

        return True, None

    def validate_features(self, feature_names: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate if all selected features exist and are available
        
        Returns: (is_valid, error_message)
        """
        if not isinstance(feature_names, list):
            return False, "Features must be provided as a list."

        for feature_name in feature_names:
            if feature_name not in self.additional_features:
                return False, f"Additional feature '{feature_name}' does not exist."

            if not self.additional_features[feature_name].available:
                return False, f"Additional feature '{feature_name}' is currently unavailable."

        return True, None

    def validate_num_members(self, num_members: int) -> Tuple[bool, Optional[str]]:
        """
        Validate number of members
        
        Returns: (is_valid, error_message)
        """
        if not isinstance(num_members, int):
            return False, "Number of members must be an integer."

        if num_members < 1:
            return False, "Number of members must be at least 1."

        if num_members > 10:
            return False, "Number of members cannot exceed 10."

        return True, None

    def calculate_base_cost(self, plan_name: str) -> float:
        """Calculate base membership cost"""
        return self.membership_plans[plan_name].base_cost

    def calculate_features_cost(self, feature_names: List[str]) -> float:
        """Calculate total cost of additional features"""
        total = 0.0
        for feature_name in feature_names:
            total += self.additional_features[feature_name].cost
        return total

    def calculate_group_discount(
        self,
        base_total: float,
        num_members: int
    ) -> Tuple[float, float]:
        """
        Calculate group discount (10% if 2+ members)
        
        Returns: (discounted_cost, discount_amount)
        """
        if num_members < self.GROUP_DISCOUNT_THRESHOLD:
            return base_total, 0.0

        discount_amount = base_total * self.GROUP_DISCOUNT_PERCENTAGE
        discounted_cost = base_total - discount_amount
        return discounted_cost, discount_amount

    def calculate_special_offer_discount(self, cost: float) -> Tuple[float, float]:
        """
        Apply special offer discounts based on cost thresholds
        
        Returns: (discounted_cost, discount_amount)
        """
        discount_amount = 0.0

        # Apply highest applicable discount
        for threshold, discount in sorted(self.SPECIAL_OFFER_DISCOUNTS, reverse=True):
            if cost > threshold:
                discount_amount = discount
                break

        discounted_cost = cost - discount_amount
        return discounted_cost, discount_amount

    def calculate_premium_surcharge(
        self,
        cost: float,
        premium_level: PremiumFeatureLevel
    ) -> Tuple[float, float]:
        """
        Apply premium surcharge (15%) if premium features selected
        
        Returns: (total_with_surcharge, surcharge_amount)
        """
        if premium_level == PremiumFeatureLevel.NONE:
            return cost, 0.0

        surcharge_amount = cost * self.PREMIUM_SURCHARGE_PERCENTAGE
        total_with_surcharge = cost + surcharge_amount
        return total_with_surcharge, surcharge_amount

    def calculate_total_cost(
        self,
        plan_name: str,
        feature_names: List[str],
        num_members: int = 1,
        premium_level: PremiumFeatureLevel = PremiumFeatureLevel.NONE
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate total membership cost with all discounts and surcharges
        
        Args:
            plan_name: Name of membership plan
            feature_names: List of additional feature names
            num_members: Number of members (for group discount)
            premium_level: Premium feature level (triggers surcharge)
        
        Returns:
            (total_cost, breakdown_dict)
            
        breakdown_dict contains:
            - base_cost: Base membership cost
            - features_cost: Total additional features cost
            - subtotal: base_cost + features_cost
            - group_discount: Amount of group discount (if applicable)
            - after_group_discount: Cost after group discount
            - special_offer_discount: Amount of special offer discount
            - after_special_discount: Cost after special offer discount
            - premium_surcharge: Amount of premium surcharge (if applicable)
            - total_cost: Final total cost
        """
        # Calculate base and features
        base_cost = self.calculate_base_cost(plan_name)
        features_cost = self.calculate_features_cost(feature_names)
        subtotal = base_cost + features_cost

        # Apply group discount
        after_group, group_discount = self.calculate_group_discount(subtotal, num_members)

        # Apply special offer discount
        after_special, special_discount = self.calculate_special_offer_discount(after_group)

        # Apply premium surcharge
        total_with_surcharge, surcharge = self.calculate_premium_surcharge(
            after_special,
            premium_level
        )

        breakdown = {
            "base_cost": base_cost,
            "features_cost": features_cost,
            "subtotal": subtotal,
            "group_discount": group_discount,
            "after_group_discount": after_group,
            "special_offer_discount": special_discount,
            "after_special_discount": after_special,
            "premium_surcharge": surcharge,
            "total_cost": total_with_surcharge,
        }

        return total_with_surcharge, breakdown

    def get_summary(
        self,
        plan_name: str,
        feature_names: List[str],
        num_members: int,
        premium_level: PremiumFeatureLevel = PremiumFeatureLevel.NONE
    ) -> str:
        """Generate a formatted summary of the membership selection"""
        total_cost, breakdown = self.calculate_total_cost(
            plan_name,
            feature_names,
            num_members,
            premium_level
        )

        summary = []
        summary.append("\n" + "=" * 60)
        summary.append("MEMBERSHIP SUMMARY".center(60))
        summary.append("=" * 60)

        summary.append(f"\nMembership Plan: {plan_name}")
        summary.append(f"Number of Members: {num_members}")

        if feature_names:
            summary.append(f"Additional Features:")
            for feature in feature_names:
                cost = self.additional_features[feature].cost
                summary.append(f"  - {feature}: ${cost:.2f}")
        else:
            summary.append("Additional Features: None")

        if premium_level != PremiumFeatureLevel.NONE:
            summary.append(f"Premium Level: {premium_level.value}")

        summary.append("\n" + "-" * 60)
        summary.append("COST BREAKDOWN".center(60))
        summary.append("-" * 60)

        summary.append(f"Base Membership Cost:        ${breakdown['base_cost']:>10.2f}")
        if breakdown['features_cost'] > 0:
            summary.append(f"Additional Features Cost:    ${breakdown['features_cost']:>10.2f}")
            summary.append(f"Subtotal:                    ${breakdown['subtotal']:>10.2f}")

        if breakdown['group_discount'] > 0:
            summary.append(f"Group Discount (10%):       -${breakdown['group_discount']:>10.2f}")
            summary.append(f"After Group Discount:        ${breakdown['after_group_discount']:>10.2f}")

        if breakdown['special_offer_discount'] > 0:
            summary.append(f"Special Offer Discount:     -${breakdown['special_offer_discount']:>10.2f}")
            summary.append(f"After Special Discount:      ${breakdown['after_special_discount']:>10.2f}")

        if breakdown['premium_surcharge'] > 0:
            summary.append(f"Premium Surcharge (15%):     ${breakdown['premium_surcharge']:>10.2f}")

        summary.append("-" * 60)
        summary.append(f"TOTAL COST:                  ${breakdown['total_cost']:>10.2f}")
        summary.append("=" * 60 + "\n")

        return "\n".join(summary)


class GymMembershipApp:
    """Command-line interface for gym membership management"""

    def __init__(self):
        """Initialize the application"""
        self.manager = GymMembershipManager()
        self.selection: Optional[MembershipSelection] = None

    def display_welcome(self) -> None:
        """Display welcome message"""
        print("\n" + "=" * 60)
        print("WELCOME TO GYM MEMBERSHIP MANAGEMENT SYSTEM".center(60))
        print("=" * 60 + "\n")

    def display_membership_plans(self) -> None:
        """Display available membership plans"""
        print("\nAvailable Membership Plans:")
        print("-" * 60)
        plans = self.manager.get_available_membership_plans()
        for i, plan in enumerate(plans, 1):
            print(f"{i}. {plan}")
        print()

    def display_additional_features(self) -> None:
        """Display available additional features"""
        print("\nAvailable Additional Features:")
        print("-" * 60)
        features = self.manager.get_available_features()
        for i, feature in enumerate(features, 1):
            print(f"{i}. {feature}")
        print()

    def select_membership_plan(self) -> Optional[str]:
        """Prompt user to select a membership plan"""
        self.display_membership_plans()
        available_plans = self.manager.get_available_membership_plans()
        plan_names = [plan.name for plan in available_plans]

        while True:
            user_input = input("Enter membership plan name or number (or 'cancel' to exit): ").strip()

            if user_input.lower() == 'cancel':
                return None

            # Check if input is a number
            if user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(plan_names):
                    return plan_names[index]
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(plan_names)}.\n")
            elif user_input in plan_names:
                return user_input
            else:
                print(f"Invalid membership plan. Please select from: {', '.join(plan_names)}\n")

    def select_additional_features(self) -> Optional[List[str]]:
        """Prompt user to select additional features"""
        self.display_additional_features()
        available_features = self.manager.get_available_features()
        feature_names = [feature.name for feature in available_features]

        selected_features = []

        while True:
            print(f"Currently selected features: {selected_features if selected_features else 'None'}")
            user_input = input(
                "Enter feature name/number to add/remove, or 'done' to continue: "
            ).strip().lower()

            if user_input == 'done':
                break
            elif user_input == 'cancel':
                return None

            # Check if input is a number
            if user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(feature_names):
                    feature_name = feature_names[index]
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(feature_names)}.\n")
                    continue
            elif user_input in feature_names:
                feature_name = user_input
            else:
                print(f"Invalid feature. Please select from: {', '.join(feature_names)}\n")
                continue

            # Toggle feature
            if feature_name in selected_features:
                selected_features.remove(feature_name)
                print(f"Removed: {feature_name}\n")
            else:
                selected_features.append(feature_name)
                print(f"Added: {feature_name}\n")

        return selected_features

    def select_num_members(self) -> Optional[int]:
        """Prompt user to enter number of members"""
        while True:
            user_input = input("Enter number of members (1-10) or 'cancel' to exit: ").strip()

            if user_input.lower() == 'cancel':
                return None

            if user_input.isdigit():
                num_members = int(user_input)
                is_valid, error_msg = self.manager.validate_num_members(num_members)
                if is_valid:
                    return num_members
                else:
                    print(f"Error: {error_msg}\n")
            else:
                print("Please enter a valid number.\n")

    def select_premium_level(self) -> Optional[PremiumFeatureLevel]:
        """Prompt user to select premium feature level"""
        print("\nPremium Feature Levels:")
        print("-" * 60)
        print("1. None")
        print("2. Exclusive Facilities Access (+15% surcharge)")
        print("3. Specialized Training Programs (+15% surcharge)")
        print()

        while True:
            user_input = input("Select premium level (1-3) or 'none' for no premium: ").strip().lower()

            if user_input in ['none', '0']:
                return PremiumFeatureLevel.NONE
            elif user_input == '1':
                return PremiumFeatureLevel.NONE
            elif user_input == '2':
                return PremiumFeatureLevel.EXCLUSIVE_FACILITIES
            elif user_input == '3':
                return PremiumFeatureLevel.SPECIALIZED_TRAINING
            else:
                print("Invalid selection. Please enter 1, 2, 3, or 'none'.\n")

    def display_potential_savings(self, plan_name: str, num_members: int) -> None:
        """Display potential savings message for group memberships"""
        if num_members >= self.manager.GROUP_DISCOUNT_THRESHOLD:
            total_without_discount, _ = self.manager.calculate_total_cost(
                plan_name, [], num_members - 1, PremiumFeatureLevel.NONE
            )
            total_with_discount, breakdown = self.manager.calculate_total_cost(
                plan_name, [], num_members, PremiumFeatureLevel.NONE
            )
            savings = breakdown['group_discount']
            print(f"\n💰 GROUP SAVINGS: Save ${savings:.2f} with {num_members} members (10% discount)!\n")

    def confirm_membership(self, summary: str) -> bool:
        """Ask user to confirm membership selection"""
        print(summary)
        while True:
            user_input = input("Do you want to confirm this membership? (yes/no): ").strip().lower()
            if user_input in ['yes', 'y']:
                return True
            elif user_input in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'.\n")

    def run(self) -> int:
        """
        Run the membership selection workflow
        
        Returns:
            Total cost as positive integer if confirmed, -1 if canceled or invalid
        """
        self.display_welcome()

        # Step 1: Select membership plan
        plan_name = self.select_membership_plan()
        if plan_name is None:
            print("Membership selection canceled.\n")
            return -1

        is_valid, error_msg = self.manager.validate_membership_plan(plan_name)
        if not is_valid:
            print(f"Error: {error_msg}\n")
            return -1

        # Step 2: Select number of members
        num_members = self.select_num_members()
        if num_members is None:
            print("Membership selection canceled.\n")
            return -1

        # Step 3: Select additional features
        feature_names = self.select_additional_features()
        if feature_names is None:
            print("Membership selection canceled.\n")
            return -1

        is_valid, error_msg = self.manager.validate_features(feature_names)
        if not is_valid:
            print(f"Error: {error_msg}\n")
            return -1

        # Step 4: Display potential savings
        self.display_potential_savings(plan_name, num_members)

        # Step 5: Select premium level
        premium_level = self.select_premium_level()
        if premium_level is None:
            print("Membership selection canceled.\n")
            return -1

        # Step 6: Generate and display summary
        summary = self.manager.get_summary(
            plan_name,
            feature_names,
            num_members,
            premium_level
        )

        # Step 7: Confirm membership
        if not self.confirm_membership(summary):
            print("Membership selection canceled. Starting over...\n")
            return self.run()

        # Step 8: Calculate and return total cost
        total_cost, _ = self.manager.calculate_total_cost(
            plan_name,
            feature_names,
            num_members,
            premium_level
        )

        final_cost = int(total_cost)
        print(f"\nMembership confirmed! Total cost: ${total_cost:.2f}\n")
        return final_cost


def main() -> int:
    """Main entry point"""
    app = GymMembershipApp()
    return app.run()


if __name__ == "__main__":
    result = main()
    print(f"Program exited with code: {result}")
