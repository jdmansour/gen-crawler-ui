"""Build a site tree from scraped breadcrumb data (jsonlines format).

Reads breadcrumb data and reconstructs the site hierarchy as a JSON tree
suitable for the SitemapTree.tsx component.

Usage:
    python build_site_tree.py bread.jsonlines > site_tree.json
"""

import json
import sys
from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """Strip trailing slash for consistent keying."""
    return url.rstrip("/")


def orient_breadcrumbs(breadcrumbs: list[dict]) -> list[dict]:
    """Return breadcrumbs in root-first order, deduplicated by URL.

    Breadcrumbs may arrive in any order (forward, reversed, or jumbled)
    and may contain duplicate URLs.  We deduplicate by normalized URL
    (keeping the last occurrence for better labels) then sort by URL
    path depth so the result is always root-first.
    """
    if not breadcrumbs:
        return breadcrumbs
    # Deduplicate by normalized URL, keeping the last occurrence
    seen: dict[str, dict] = {}
    for crumb in breadcrumbs:
        seen[normalize_url(crumb["url"])] = crumb
    deduped = list(seen.values())
    deduped.sort(key=lambda c: normalize_url(c["url"]).count("/"))
    return deduped


def url_to_id(url: str) -> str:
    """Convert a URL to a stable id by using its path segments."""
    path = urlparse(normalize_url(url)).path.strip("/")
    if not path:
        return "root"
    return path.replace("/", "-")


def build_tree(input_path: str) -> list[dict]:
    # url -> {id, label, url, children_map}  (children_map is url -> node)
    nodes: dict[str, dict] = {}
    used_ids: dict[str, int] = {}  # base_id -> count, for uniqueness

    def make_unique_id(url: str) -> str:
        base = url_to_id(url)
        count = used_ids.get(base, 0)
        used_ids[base] = count + 1
        return base if count == 0 else f"{base}--{count}"

    def get_or_create(url: str, label: str) -> dict:
        key = normalize_url(url)
        if key not in nodes:
            nodes[key] = {
                "id": make_unique_id(url),
                "label": label,
                "url": key,
                "children_map": {},  # url -> node, preserves insertion order
            }
        return nodes[key]

    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if not entry.get("breadcrumbs"):
                continue
            # Filter out breadcrumb entries with null/missing URLs
            valid = [c for c in entry["breadcrumbs"] if c.get("url")]
            crumbs = orient_breadcrumbs(valid)
            # Only trust breadcrumbs up to the page's own URL
            page_url = normalize_url(entry["url"])
            crumbs = [
                c for c in crumbs
                if normalize_url(c["url"]).count("/") <= page_url.count("/")
            ]

            # Walk the breadcrumb chain, linking parent -> child
            for i, crumb in enumerate(crumbs):
                node = get_or_create(crumb["url"], crumb["name"])
                if i > 0:
                    parent_url = normalize_url(crumbs[i - 1]["url"])
                    child_key = normalize_url(crumb["url"])
                    if child_key != parent_url:
                        parent = nodes[parent_url]
                        if child_key not in parent["children_map"]:
                            parent["children_map"][child_key] = node

    # Find root nodes (nodes that are never a child of another node)
    all_child_keys: set[str] = set()
    for node in nodes.values():
        all_child_keys.update(node["children_map"].keys())
    root_keys = [k for k in nodes if k not in all_child_keys]

    def to_tree_item(node: dict, visited: set[str] | None = None) -> dict:
        if visited is None:
            visited = set()
        item: dict = {"id": node["id"], "label": node["label"], "url": node["url"]}
        visited.add(node["id"])
        children = [
            child for child in node["children_map"].values()
            if child["id"] not in visited
        ]
        if children:
            item["children"] = [
                to_tree_item(child, visited) for child in children
            ]
        return item

    return [to_tree_item(nodes[k]) for k in root_keys]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.jsonlines>", file=sys.stderr)
        sys.exit(1)
    tree = build_tree(sys.argv[1])
    json.dump(tree, sys.stdout, indent=2, ensure_ascii=False)
    print()  # trailing newline
