import os
import random
import sys

# The way obsidian lab runs is weird. Maybe run directly with flask instead.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# obsidiantools requirements
import numpy as np
import pandas as pd
import networkx as nx
import obsidiantools.api as otools  # api shorthand

from lib import use_similarity

from pathlib import Path


def intersects(lst1, lst2):
    for value in lst1:
        if value in lst2:
            return True
    return False


def check_has_common_tags(first, second, vault):
    tags1 = vault.get_tags(first)
    tags2 = vault.get_tags(second)
    return intersects(tags1, tags2)


def check_has_link(first, second, vault):
    backs1 = vault.get_backlinks(first)
    backs2 = vault.get_backlinks(second)
    if first in backs2:
        return True
    if second in backs1:
        return True
    return False


def trim_string(s: str, limit: int, ellipsis="…") -> str:
    s = s.strip()
    if len(s) > limit:
        return s[:limit].strip() + ellipsis
    return s


FULL_IGNORES = ["root"]


def to_lab_ui(pairs, vault):
    # Sort tuples by score.
    pairs.sort(key=lambda x: x[2], reverse=True)
    items = []
    for fir, sec, score in pairs:
        has_common = check_has_common_tags(fir, sec, vault)
        has_link = check_has_link(fir, sec, vault)
        if (fir in FULL_IGNORES) or (sec in FULL_IGNORES) or has_common or has_link:
            continue

        # Turn each tuple into multiple UI entries for LAB.

        # Build first name with score.
        scostr = trim_string(str(score * 100), 2) + " "
        # Optional markers for showing existing relationships.
        link = "@" if has_link else "-"
        tag = "#" if has_common else "-"

        items.append(
            {
                # Build path for linking with name and vault path.
                "path": os.path.join(vault.dirpath, fir + ".md"),
                "name": fir,
                "info": {"score": score},
            }
        )

        items.append(
            {
                # Build path for linking with name and vault path.
                "path": os.path.join(vault.dirpath, sec + ".md"),
                "name": sec,
                "info": {"score": score},
            }
        )

        # Dummy to have more separation between the items
        dummy_gap = {
            # Build path for linking with name and vault path.
            "path": os.path.join(vault.dirpath, sec + ".md"),
            "name": "",
            "info": {"score": score},
        }
        items.append(dummy_gap)
        items.append(dummy_gap)
        items.append(dummy_gap)
        items.append(dummy_gap)
    return items


class Plugin:
    vault_path = ""
    max_results = 20

    # Currently Obsidian Lab seems to run this on every request - look into caching the vault processing results and preloading them instead.
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.plugin_name = os.path.basename(__file__)
        super()

    def execute(self, args):
        print("request", self.plugin_name, args)
        # Example args: {'vaultPath': '', 'notePath': 'blah.md'}

        vault_dir = Path(self.vault_path)
        self.vault = otools.Vault(vault_dir).connect().gather()

        # Include the note title to be analyzed.
        def get_full_text(name):
            text = self.vault.get_text(name)
            return name + ". " + text

        documents = {name: get_full_text(name) for name in self.vault.file_index.keys()}

        print("Files imported")

        self.use_results = use_similarity.top_pairs(documents, 30)

        print("USE scores ready")

        items = to_lab_ui(self.use_results, self.vault)

        return {
            "contents": items,
        }
