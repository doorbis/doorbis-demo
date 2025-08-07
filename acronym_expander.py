# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 14:28:16 2025

@author: o4-mini-high
"""

import re

def load_acronyms(filepath='Acronymns.txt'):
    """
    Reads acronyms from a Markdown table file and returns a list of acronyms.
    Assumes the first column of each table row is the acronym (possibly wrapped in **bold**).
    """
    acronyms = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip header/separator lines
            if not line.startswith('|') or set(line) <= {'|', '-', ' '}:
                continue
            # Split columns by '|'
            parts = [p.strip() for p in line.split('|')]
            # parts[1] is the first data column
            if len(parts) >= 2 and parts[1]:
                # Remove Markdown bold markers **
                acronym = parts[1].strip('*')
                acronyms.append(acronym)
    return acronyms


# Load once at import
def _build_pattern(filepath='Acronymns.txt'):
    acrs = load_acronyms(filepath)
    # Create regex to match any acronym as a whole word
    pattern = r'\b(' + '|'.join(map(re.escape, acrs)) + r')\b'
    return re.compile(pattern)

_PATTERN = _build_pattern()


def acronym_expander(raw_text):
    """
    Replaces each acronym (from the Acronymns.txt file) in raw_text
    with its individual characters separated by single spaces.
    Other text remains unchanged.
    """
    def _expand(match):
        return ' '.join(match.group(0))
    return _PATTERN.sub(_expand, raw_text)


# Example usage
if __name__ == '__main__':
    sample = "The HOA and HUD regulations require an MLS listing to calculate ROI."
    print(acronym_expander(sample))  # -> The H O A and H U D regulations require an M L S listing to calculate R O I.
