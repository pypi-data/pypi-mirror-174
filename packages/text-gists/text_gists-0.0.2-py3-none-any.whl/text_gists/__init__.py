__version__ = "0.0.1"
from .__main__ import (
    construct_indicators,
    cull_suffix,
    get_first_matching_text_of_regex,
    if_match_found_return_text,
    remove_pattern_if_found_else_text,
    text_in_pattern_count,
    trim_text,
)
from .constructors import (
    combine_regexes_as_options,
    construct_acronyms,
    construct_negative_lookbehinds,
    construct_prefix_options,
)
