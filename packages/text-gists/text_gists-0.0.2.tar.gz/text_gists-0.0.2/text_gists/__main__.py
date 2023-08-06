import re
from typing import Iterator, Pattern


def construct_indicators(*args: str) -> Pattern:
    """For each regex string passed (with `re.X`|`VERBOSE` flag enabled), create a group as a possible option; then return constructed Pattern.

    Returns:
        Pattern: A pattern object based on joined regex strings
    """
    regex_strings: Iterator = (rf"({i})" for i in args)
    regex_combined: str = "|".join(regex_strings)
    pattern = re.compile(regex_combined, re.X)
    return pattern


def if_match_found_return_text(p: Pattern, text: str) -> str | None:
    """If pattern `p` matches anything in text, return portion of text matched"""
    if match := p.search(text):
        return match.group(0)
    return None


def get_first_matching_text_of_regex(regex: str, text: str) -> str | None:
    """Construct pattern object from regex string with (with `re.X`|`VERBOSE` flag enabled), return portion of text matched"""
    pattern = re.compile(regex, re.X)
    matched_text = if_match_found_return_text(pattern, text)
    return matched_text


def text_in_pattern_count(p: Pattern, text_to_query: str) -> int:
    """Return count of number of times the `pattern` matches in the text

    Args:
        p (Pattern): A compiled regex object
        text_to_query (str): String to find matches on

    Returns:
        int: Number of times the pattern appears in a given text.
    """
    patterns_found = p.finditer(text_to_query)
    patterns = list(patterns_found)
    counted = len(patterns)
    return counted


def remove_pattern_if_found_else_text(p: Pattern, text: str) -> str:
    """Remove a `pattern` found in text"""
    return p.sub("", text) if p.search(text) else text


def cull_suffix(text: str) -> str:
    """Remove `the`, `of`, `,`, ` ` from the text's suffix, when existing text is passed"""
    for i in ["the", "of", ","]:
        text = text.removesuffix(i).strip()
    return text


def trim_text(raw: str, max_length: int) -> str:
    """Given a max length for a text, limit text to the same if it exceeds the length"""
    return raw[:max_length] if len(raw) > max_length else raw
