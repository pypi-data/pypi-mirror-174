from panther_sdk import testing
from panther_utils import match_filters


class TestMatchFilters(testing.PantherPythonFilterTestCase):
    def test_deep_exists(self) -> None:
        test_filter = match_filters.deep_exists("a.b")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterNotMatches(test_filter, {"a": {"c": "other-value"}})

    def test_deep_not_exists(self) -> None:
        test_filter = match_filters.deep_not_exists("a.b")

        self.assertFilterIsValid(test_filter)

        self.assertFilterNotMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterMatches(test_filter, {"a": {"c": "other-value"}})

    def test_deep_equal(self) -> None:
        test_filter = match_filters.deep_equal("a.b", "targeted-value")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_not_equal(self) -> None:
        test_filter = match_filters.deep_not_equal("a.b", "targeted-value")

        self.assertFilterIsValid(test_filter)

        self.assertFilterNotMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_in(self) -> None:
        test_filter = match_filters.deep_in("a.b", ["targeted-value"])

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_not_in(self) -> None:
        test_filter = match_filters.deep_not_in("a.b", ["targeted-value"])

        self.assertFilterIsValid(test_filter)

        self.assertFilterNotMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_equal_pattern(self) -> None:
        test_filter = match_filters.deep_equal_pattern("a.b", r"target")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_not_equal_pattern(self) -> None:
        test_filter = match_filters.deep_not_equal_pattern("a.b", r"target")

        self.assertFilterIsValid(test_filter)

        self.assertFilterNotMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_less_than(self) -> None:
        test_filter = match_filters.deep_less_than("a.b", 45)

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": 44}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 45}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 46}})

    def test_deep_less_than_or_equal(self) -> None:
        test_filter = match_filters.deep_less_than_or_equal("a.b", 45)

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": 44}})
        self.assertFilterMatches(test_filter, {"a": {"b": 45}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 46}})

    def test_deep_greater_than(self) -> None:
        test_filter = match_filters.deep_greater_than("a.b", 45)

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": 46}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 45}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 44}})

    def test_deep_greater_than_or_equal(self) -> None:
        test_filter = match_filters.deep_greater_than_or_equal("a.b", 45)

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": 46}})
        self.assertFilterMatches(test_filter, {"a": {"b": 45}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 44}})

    def test_deep_between(self) -> None:
        test_filter = match_filters.deep_between("a.b", val_min=45, val_max=50)

        self.assertFilterIsValid(test_filter)

        self.assertFilterNotMatches(test_filter, {"a": {"b": 44}})

        self.assertFilterMatches(test_filter, {"a": {"b": 45}})
        self.assertFilterMatches(test_filter, {"a": {"b": 46}})
        self.assertFilterMatches(test_filter, {"a": {"b": 49}})
        self.assertFilterMatches(test_filter, {"a": {"b": 50}})

        self.assertFilterNotMatches(test_filter, {"a": {"b": 51}})

        self.assertRaises(RuntimeError, lambda: match_filters.deep_between("x", 45, 45))
        self.assertRaises(RuntimeError, lambda: match_filters.deep_between("x", 45, 44))

    def test_deep_between_exclusive(self) -> None:
        test_filter = match_filters.deep_between_exclusive(
            "a.b", val_min=45, val_max=50
        )

        self.assertFilterIsValid(test_filter)

        self.assertFilterNotMatches(test_filter, {"a": {"b": 44}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 45}})

        self.assertFilterMatches(test_filter, {"a": {"b": 46}})
        self.assertFilterMatches(test_filter, {"a": {"b": 49}})

        self.assertFilterNotMatches(test_filter, {"a": {"b": 50}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": 51}})

        self.assertRaises(
            RuntimeError, lambda: match_filters.deep_between_exclusive("x", 45, 45)
        )
        self.assertRaises(
            RuntimeError, lambda: match_filters.deep_between_exclusive("x", 45, 44)
        )
