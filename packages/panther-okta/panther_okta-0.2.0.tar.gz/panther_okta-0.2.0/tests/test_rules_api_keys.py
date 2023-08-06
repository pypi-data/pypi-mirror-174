import unittest

from panther_sdk import detection
import panther_okta as okta


class TestRulesAPIKeys(unittest.TestCase):
    def test_api_key_revoked(self) -> None:
        name_override = "Override Name"
        rule = okta.rules.api_key_revoked(
            overrides=detection.RuleOptions(name=name_override)
        )

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.name, name_override)

    def test_api_key_created(self) -> None:
        name_override = "Override Name"
        rule = okta.rules.api_key_created(
            overrides=detection.RuleOptions(name=name_override)
        )

        self.assertIsInstance(rule, detection.Rule)
        self.assertEqual(rule.name, name_override)
