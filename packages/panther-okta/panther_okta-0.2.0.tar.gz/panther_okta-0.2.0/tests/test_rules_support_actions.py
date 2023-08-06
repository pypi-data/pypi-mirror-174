import unittest

from panther_sdk import detection
import panther_okta as okta


class TestSupportActions(unittest.TestCase):
    def test_account_support_access_defaults(self) -> None:
        rule = okta.rules.account_support_access()

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.rule_id, "Okta.Support.Access")

    def test_account_support_access_name_override(self) -> None:
        name_override = "Access Granted for Okta Support"
        rule = okta.rules.account_support_access(
            overrides=detection.RuleOptions(name=name_override)
        )

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.name, name_override)

    def test_account_support_reset(self) -> None:
        name_override = "Override Name"
        rule = okta.rules.support_reset(
            overrides=detection.RuleOptions(name=name_override)
        )

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.name, name_override)
