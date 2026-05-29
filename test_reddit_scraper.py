import pytest

from reddit_scraper import validate_subreddits, _SUBREDDIT_NAME_PATTERN


class TestSubredditNamePattern:
    """Tests for the regex pattern itself."""

    def test_valid_lowercase(self):
        assert _SUBREDDIT_NAME_PATTERN.match("stocks")

    def test_valid_mixed_case(self):
        assert _SUBREDDIT_NAME_PATTERN.match("StockMarket")

    def test_valid_with_underscore(self):
        assert _SUBREDDIT_NAME_PATTERN.match("penny_stocks")

    def test_valid_with_numbers(self):
        assert _SUBREDDIT_NAME_PATTERN.match("wsb2024")

    def test_valid_min_length(self):
        assert _SUBREDDIT_NAME_PATTERN.match("abc")

    def test_valid_max_length(self):
        assert _SUBREDDIT_NAME_PATTERN.match("a" * 21)

    def test_invalid_too_short(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("ab")

    def test_invalid_too_long(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("a" * 22)

    def test_invalid_starts_with_underscore(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("_stocks")

    def test_invalid_contains_space(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("wall street")

    def test_invalid_contains_hyphen(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("penny-stocks")

    def test_invalid_contains_special_chars(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("stocks!")

    def test_invalid_empty_string(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("")

    def test_invalid_contains_slash(self):
        assert not _SUBREDDIT_NAME_PATTERN.match("r/stocks")


class TestValidateSubreddits:
    """Tests for the validate_subreddits function."""

    def test_valid_list(self):
        result = validate_subreddits(["wallstreetbets", "stocks", "investing"])
        assert result == ["wallstreetbets", "stocks", "investing"]

    def test_returns_same_list(self):
        input_list = ["stocks", "investing"]
        assert validate_subreddits(input_list) is input_list

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_subreddits([])

    def test_invalid_name_too_short(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits(["ab"])

    def test_invalid_name_too_long(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits(["a" * 22])

    def test_invalid_name_starts_with_underscore(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits(["_badname"])

    def test_invalid_name_with_spaces(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits(["wall street bets"])

    def test_invalid_name_with_special_chars(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits(["stocks!"])

    def test_invalid_name_with_slash(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits(["r/stocks"])

    def test_non_string_in_list(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits([123])  # type: ignore[list-item]

    def test_multiple_invalid_names_reported(self):
        with pytest.raises(ValueError, match="Invalid subreddit name") as exc_info:
            validate_subreddits(["ab", "stocks", "r/bad"])
        assert "ab" in str(exc_info.value)
        assert "r/bad" in str(exc_info.value)

    def test_mix_of_valid_and_invalid(self):
        with pytest.raises(ValueError, match="Invalid subreddit name"):
            validate_subreddits(["stocks", "!!bad", "investing"])

    def test_single_valid_name(self):
        assert validate_subreddits(["stocks"]) == ["stocks"]

    def test_valid_names_with_underscores(self):
        assert validate_subreddits(["the_gang", "penny_stocks"]) == [
            "the_gang",
            "penny_stocks",
        ]
