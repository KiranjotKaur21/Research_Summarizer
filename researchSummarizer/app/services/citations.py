import re
from typing import List, Tuple

# numeric [1], [1,2]
RE_NUMERIC_BRACKETS = re.compile(r"\[(?:\s*\d+\s*(?:,\s*\d+\s*)*)\]")

# parenthetical like (Smith, 2019)
RE_PAREN_YEAR = re.compile(r"\(\s*[A-Z][A-Za-z\-,\s\.]+,\s*\d{4}\s*\)")

# author-year like "Smith et al., 2020" or "Smith, 2020" or "Smith & Lee, 2020"
RE_AUTHOR_YEAR = re.compile(
    r"""
    (?P<full>                                     # capture the whole citation
      \b                                          # word boundary
      [A-Z][A-Za-z\-\']+                          # surname (starts with capital)
      (?:                                       
        (?:\s+(?:et\ al\.|and|&)\s+[A-Z][A-Za-z\-\']+)?   # optional "et al." or "& Lastname"
      )?
      (?:                                       # allow multiple authors separated by commas or "and"
        (?:\s*,\s*[A-Z][A-Za-z\-\']+)*         
      ) 
      (?:,\s*)?                                  # optional comma before year
      (?:\(?\d{4}\)?)                            # year, maybe in parentheses
    )
    """,
    re.VERBOSE,
)


def _unique_preserve_order(seq: List[str]) -> List[str]:
    seen = set()
    out = []
    for s in seq:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def extract_citations(text: str) -> List[str]:
    if not text:
        return []

    found: List[str] = []

    for m in RE_NUMERIC_BRACKETS.finditer(text):
        found.append(m.group(0))

    for m in RE_PAREN_YEAR.finditer(text):
        found.append(m.group(0))

    for m in RE_AUTHOR_YEAR.finditer(text):
        s = m.group("full").strip()
        found.append(s)

    return _unique_preserve_order(found)

def strip_citations(text: str) -> Tuple[str, List[str]]:
    if not text:
        return "", []

    citations = extract_citations(text)

    clean = text
    clean = RE_NUMERIC_BRACKETS.sub(" ", clean)
    clean = RE_PAREN_YEAR.sub(" ", clean)
    clean = RE_AUTHOR_YEAR.sub(" ", clean)

    clean = re.sub(r"\s{2,}", " ", clean).strip()

    return clean, citations
