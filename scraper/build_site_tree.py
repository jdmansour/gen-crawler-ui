"""Build a site tree from scraped breadcrumb data (jsonlines format).

Reads breadcrumb data and reconstructs the site hierarchy as a JSON tree
suitable for the SitemapTree.tsx component.

Usage:
    python build_site_tree.py bread.jsonlines > site_tree.json
    python build_site_tree.py --base-url https://de.serlo.org bread-serlo.jsonlines > serlo.json
    python build_site_tree.py --no-reorder bread.jsonlines > site_tree.json
"""

import argparse
import json
import sys
from urllib.parse import urljoin, urlparse


def normalize_url(url: str) -> str:
    """Strip trailing slash for consistent keying."""
    return url.rstrip("/")


def resolve_url(url: str, base_url: str | None) -> str:
    """Resolve a possibly-relative URL against a base URL."""
    if base_url and url:
        return urljoin(base_url, url)
    return url


def dedup_breadcrumbs(breadcrumbs: list[dict]) -> list[dict]:
    """Deduplicate breadcrumbs by normalized URL, preserving original order.

    Keeps the last occurrence of each URL (for better labels).
    """
    if not breadcrumbs:
        return breadcrumbs
    # Walk backwards so the last occurrence wins, then reverse to restore order
    seen: dict[str, dict] = {}
    for crumb in reversed(breadcrumbs):
        key = normalize_url(crumb["url"])
        if key not in seen:
            seen[key] = crumb
    # Return in original order (first occurrence position of each unique URL)
    result = []
    seen_keys: set[str] = set()
    for crumb in breadcrumbs:
        key = normalize_url(crumb["url"])
        if key not in seen_keys:
            seen_keys.add(key)
            result.append(seen[key])  # use the last-occurrence's data (better label)
    return result


def reorder_breadcrumbs(breadcrumbs: list[dict]) -> list[dict]:
    """Sort breadcrumbs root-first by URL path depth.

    Use this when breadcrumbs may arrive in any order (reversed, jumbled).
    Only valid when URL path depth reflects hierarchy depth.
    """
    if not breadcrumbs:
        return breadcrumbs
    return sorted(breadcrumbs, key=lambda c: normalize_url(c["url"]).count("/"))


def url_to_id(url: str) -> str:
    """Derive a human-readable ID from a URL's path (e.g. 'mathe-algebra')."""
    path = urlparse(normalize_url(url)).path.strip("/")
    return path.replace("/", "-") if path else "root"


def build_tree(input_path: str, base_url: str | None = None,
               reorder: bool = True) -> list[dict]:
    """Read breadcrumb jsonlines and return a tree of {id, label, url, children}.

    Args:
        input_path: Path to a .jsonlines file with breadcrumb data.
        base_url:   Optional base URL for resolving relative breadcrumb URLs
                    (e.g. "https://de.serlo.org").
        reorder:    If True, sort breadcrumbs by URL depth (assumes path depth
                    reflects hierarchy). If False, trust the source order.
    """
    # -- Node storage and ID generation --
    nodes: dict[str, dict] = {}          # normalized_url -> node dict
    assigned_ids: set[str] = set()       # all IDs in use (for collision checks)
    id_counters: dict[str, int] = {}     # base_id -> next suffix to try

    def make_unique_id(url: str) -> str:
        """Generate a unique node ID from a URL, handling collisions."""
        base = url_to_id(url)
        if base not in assigned_ids:
            assigned_ids.add(base)
            id_counters[base] = 1
            return base
        # Find the next available suffixed ID
        n = id_counters.get(base, 1)
        candidate = f"{base}--{n}"
        while candidate in assigned_ids:
            n += 1
            candidate = f"{base}--{n}"
        id_counters[base] = n + 1
        assigned_ids.add(candidate)
        return candidate

    def get_or_create(url: str, label: str) -> dict:
        """Return an existing node for this URL, or create a new one."""
        key = normalize_url(url)
        if key not in nodes:
            nodes[key] = {
                "id": make_unique_id(url),
                "label": label,
                "url": key,
                "children_map": {},
            }
        return nodes[key]

    # -- Read and process breadcrumb entries --
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if not entry.get("breadcrumbs"):
                continue

            # Drop breadcrumbs without a URL, then resolve relative URLs
            valid = [c for c in entry["breadcrumbs"] if c.get("url")]
            if base_url:
                for crumb in valid:
                    crumb["url"] = resolve_url(crumb["url"], base_url)

            # Deduplicate (always), reorder (optional)
            crumbs = dedup_breadcrumbs(valid)
            if reorder:
                crumbs = reorder_breadcrumbs(crumbs)

                # Only trust breadcrumbs up to the page's own URL depth
                # (only meaningful when paths reflect hierarchy)
                page_url = normalize_url(resolve_url(entry["url"], base_url))
                crumbs = [
                    c for c in crumbs
                    if normalize_url(c["url"]).count("/") <= page_url.count("/")
                ]

            # Walk the breadcrumb chain, linking parent -> child
            for i, crumb in enumerate(crumbs):
                node = get_or_create(crumb["url"], crumb["name"])
                if i > 0:
                    parent_key = normalize_url(crumbs[i - 1]["url"])
                    child_key = normalize_url(crumb["url"])
                    if child_key != parent_key:  # skip self-loops
                        parent = nodes[parent_key]
                        if child_key not in parent["children_map"]:
                            parent["children_map"][child_key] = node

    # -- Build output tree --
    # Root nodes are those never referenced as a child of another node
    all_child_keys: set[str] = set()
    for node in nodes.values():
        all_child_keys.update(node["children_map"].keys())
    root_keys = [k for k in nodes if k not in all_child_keys]

    def to_tree_item(node: dict, visited: set[str]) -> dict:
        """Convert internal node dict to output format, breaking cycles."""
        item: dict = {"id": node["id"], "label": node["label"], "url": node["url"]}
        visited.add(node["id"])
        # Re-check visited before each recursive call: a sibling's subtree
        # may have already claimed a child node.
        child_items = []
        for child in node["children_map"].values():
            if child["id"] not in visited:
                child_items.append(to_tree_item(child, visited))
        if child_items:
            item["children"] = child_items
        return item

    # Share visited set across all roots to prevent the same node
    # appearing in multiple subtrees
    visited: set[str] = set()
    return [to_tree_item(nodes[k], visited) for k in root_keys]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build a site tree from scraped breadcrumb data."
    )
    parser.add_argument("input", help="Path to input .jsonlines file")
    parser.add_argument(
        "--base-url",
        default=None,
        help="Base URL for resolving relative breadcrumb URLs "
             "(e.g. https://de.serlo.org)",
    )
    parser.add_argument(
        "--no-reorder",
        action="store_true",
        help="Trust breadcrumb order from source instead of sorting by URL depth",
    )
    args = parser.parse_args()
    tree = build_tree(args.input, base_url=args.base_url, reorder=not args.no_reorder)
    json.dump(tree, sys.stdout, indent=2, ensure_ascii=False)
    print()
