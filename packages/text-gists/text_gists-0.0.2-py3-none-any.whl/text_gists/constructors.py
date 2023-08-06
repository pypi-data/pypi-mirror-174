from typing import Iterator


def get_regexes(regexes: list[str], negate: bool = False) -> Iterator[str]:
    for x in regexes:
        yield rf"(?<!{x}\s)" if negate else x


def combine_regexes_as_options(regexes: list[str]) -> str:
    texts = get_regexes(regexes)  # no negation
    joined = "|".join(texts)  # with pipe
    return rf"({joined})"  # no space


def construct_prefix_options(regex: str, options: list[str]) -> str:
    texts = get_regexes(options)  # no negation
    joined = "|".join(texts)  # with pipe
    return rf"({joined})\s{regex}"  # with space


def construct_negative_lookbehinds(regex: str, lookbehinds: list[str]) -> str:
    negated_with_space = get_regexes(lookbehinds, negate=True)  # with negation
    negations = "".join(negated_with_space)  # no pipe
    return rf"{negations}({regex})"  # no space


def construct_acronyms(text: str, year: int | None = None) -> str:
    uppered = "".join(x.upper() for x in text)
    perioded = "".join(rf"{x}\." for x in uppered)
    acronyms = rf"({uppered}\b|{perioded})"
    if year:
        acronyms = rf"{str(year)}\s+{acronyms}"
    return acronyms
