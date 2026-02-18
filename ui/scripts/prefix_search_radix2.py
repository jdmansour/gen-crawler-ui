import argparse
from itertools import islice
import math
import os
import re
import sys
from pathlib import Path
from typing import Iterator

import django

django_root = Path(__file__).resolve().parents[1]
sys.path.append(str(django_root))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler_ui.settings")
django.setup()

from crawls.models import CrawledURL, FilterSet
from scripts.radix import RadixTree, BranchInfo

def main():
    # parse arguments like:
    # python scriptname.py --filterset=10

    parser = argparse.ArgumentParser(description='Finds common prefixes and adds them to a filterset.')
    parser.add_argument('--filterset', type=int, help='The filterset to use', required=True)
    args = parser.parse_args()
    # print(args.filterset)
    
    prefixes = find_new_prefixes(args.filterset)
    for prefix in prefixes:
        print(prefix)

def find_new_prefixes(filterset_id: int):

    filterset = FilterSet.objects.get(pk=filterset_id)
    # get the latest crawl job with crawl_type="EXPLORATION" for this filterset
    # Include both COMPLETED and CANCELED jobs, as canceled jobs may still have useful data
    crawler = filterset.crawler
    job = crawler.crawl_jobs.filter(
        crawl_type="EXPLORATION",
        state__in=["COMPLETED", "CANCELED"]
    ).order_by('-created_at').first()
    #job = filterset.crawl_job
    max_prefixes = 10

    #job = CrawlJob.objects.get(pk=9)
    # job = CrawlJob.objects.get(pk=6)
    urls = CrawledURL.objects.filter(crawl_job=job)
    # for url in urls[0:10]:
    #     print(url.url)
    
    tree = RadixTree()
    for url in urls:  # [:50000]:
        tree.insert(url.url)
    
    # # tuples of (nleaves, nchildren, value)
    # branchlist = []

    # def count_leaves(node: RadixNode, prefix, branchlist):
    #     count = 0
    #     if node.is_leaf:
    #         count += 1
    #     for key, child in node.children.items():
    #         count += count_leaves(child, prefix + key, branchlist)
    #     nchildren = len(node.children)
    #     branchlist.append((count, nchildren, prefix, node.is_leaf))
    #     return count
    
    # # print("  Leaves  Children  Node")
    # count_leaves(tree._store, "", branchlist)

    branchlist = tree.calculate_branchlist()
    prefixes = find_best_prefixes(branchlist)
    prefixes_returned = 0
    for info in prefixes:
        # prefix = info.prefix
        # score = score_function(info)
        # print(f"{count:>8} {nchildren:>9} ({score:4.2f}) {prefix}")

        # check if the prefix is already in the filterset
        # is there a FilterRule with rule == prefix?
        if FilterSet.objects.filter(rules__rule=info.prefix, id=filterset.id).exists():
            # print("Already in filterset:", info.prefix)
            continue

        # print(info.prefix)
        prefixes_returned += 1
        yield info.prefix
        if prefixes_returned >= max_prefixes:
            break


# return an enumerator of tuples
def find_best_prefixes(branchlist: list[BranchInfo]) -> Iterator[BranchInfo]:
    branchlist.sort(key=score_function, reverse=True)
    already_printed = []
    for i, info in enumerate(branchlist):
        # (count, nchildren, prefix, is_leaf) = info
        prefix = info.prefix
        # if not prefix.startswith("https://www.weltderphysik.de/gebiet/te"):
        #     continue
        # if prefix == "" or prefix == "https://www.weltderphysik.de/":
        #     continue
        if i > 1 and any(prefix.startswith(ap) for ap in already_printed):
            # print(f"{count:>8} {nchildren:>9} ({score((count, nchildren, prefix)):4.2f}) {prefix} (already printed)")
            continue
        # print(f"{count:>8} {nchildren:>9} ({score_function((count, nchildren, prefix, is_leaf)):4.2f}) {prefix}")
        yield info
        already_printed.append(prefix)

# sort by number of leaves
def score_function(entry: BranchInfo) -> float:
    try:
        count, nchildren, prefix, is_leaf = entry
    except Exception:
        print("entry:", entry)
        raise
    
    baseurl, _, query = prefix.partition("?")
    score = 1
    # prefer more leaves
    score = score * count
    # prefer less direct children
    score = score / math.sqrt(nchildren+1)
    # prefer shorter query strings (?a=b&c=d)
    score = score / (len(query) + 1)
    # prefer longer urls
    # score = score * (len(baseurl) + 1)
    # # prefer shorter urls
    score = score / (len(baseurl) + 1)
    # disqualify empty prefix (root node)
    if prefix == "" or prefix == "https://www.weltderphysik.de/":
        score = 0

    # if "wiki/Spezial:" in prefix:
    #     score = score * 10

    # if re.search(r"/wiki/[a-zA-Z0-9_\-]+:", prefix):
    #     score = score * 10


    if baseurl.endswith("/"):
        score *= 5

    # strip off protocol
    baseurl_noprot = re.sub(r"^https?://", "", baseurl)
    parts = baseurl_noprot.strip("/").split("/")
    if len(parts) == 1:
        score = 0
    # # prefer more parts
    # score *= (len(parts)+1)

    # parts = baseurl.strip("/").split("/")
    # prefer more parts
    # score *= (len(parts)+1)
    # prefer longer last part
    # score *= (len(parts[-1])+1)

    # parts2 = re.split(r"[:/]", baseurl)
    # # prefer more parts
    # score *= (len(parts2)+1)

    # prefer leaf nodes
    if is_leaf:
        score *= 5

    # specials = [
    #     "impressum", "datenschutz", "kontakt", "ueber-uns", "about"
    # ]
    # if any(special in baseurl.lower() for special in specials):
    #     score = score * 10
    # # for special in specials:
    # #     if special in baseurl.lower():
    # #         score = score * 10

    # baseurl.strip(":/")
    # # split at last : or /
    # if m := re.search(r"[^:/]*$", baseurl):
    #     lastpart = m.group(0)
    #     firstpart = baseurl[:-len(lastpart)]
    #     # print("firstpart:", firstpart, "lastpart:", lastpart)
    #     score = score * (len(firstpart)+1) / (len(lastpart)+1)
    #     # if len(lastpart) < 5:
    #     #     score = score / 20



    # # check if we can reduce the prefix while keeping the same number of leaves
    
    # node, remainder = tree.locate_insertion_point(prefix)
    # print("remainder:", remainder)

    if nchildren <= 5:
        score /= 5
    number_at_end = re.compile(r"(\d+)/?$")
    if m := number_at_end.search(baseurl):
        # score = 500
        if len(m.group(1)) == 4:
            # How many articles do we expect per year?
            # score = score / 24
            pass
        else:
            # penalize if it looks like a cut off year number
            # score = score / 24 / 5
            score = score / 5
    
    # if prefix == "https://www.weltderphysik.de/gebiet/technik/":
    #     score = 1180
    return score

def find_patterns(incoming_urls):
    urls = {}
    # make the tree
    for url in incoming_urls:
        atype = None
        # url, atype = line.strip().split("____")  # assuming incoming_urls is a list with each entry of type url__class
        if len(url) < 100:   # Take only the initial 100 characters to avoid building a sparse tree
            bound = len(url) + 1
        else:
            bound = 101
        for x in range(1, bound):
            prefix = url[:x].lower()
            if prefix not in urls:
                urls[prefix] = {'positive': 0, 'negative': 0, 'total': 0}
            if atype:
                urls[prefix][atype] += 1
            urls[prefix]['total'] += 1

    new_urls = {}
    # prune the tree
    for url, data in urls.items():
        if data['total'] < 5:  # For something to be called as common pattern, there should be at least 5 occurrences of it.
            continue
        data['negative_percentage'] = (float(data['negative']) * 100) / data['total']
        # if data['negative_percentage'] < 85.0: # Assuming I am interested in finding url patterns for negative class
        #     continue
        length = len(url)
        found = False
        # iterate to see if a len+1 url is present with same total count
        for second, seconddata in urls.items():
            if len(second) <= length:
                continue
            if url == second[:length] and data['total'] == seconddata['total']:
                found = True
                break
        # discard urls with length less than 20
        if not found: #  and len(url) > 20:
            new_urls[url] = data

    print("URL Pattern; Positive; Negative; Total; Negative (%)")
    for url, data in new_urls.items():
        print("%s; %d; %d; %d; %.2f" % (
            url, data['positive'], data['negative'], data['total'],
            data['negative_percentage']))

    # example prefix:
    # https://www.weltderphysik.de/gebiet/te; 0; 0; 161; 0.00
    # we want to find:
    # https://www.weltderphysik.de/gebiet/teilchen/; 0; 0; 117; 0.00
    # https://www.weltderphysik.de/gebiet/technik/; 0; 0; 44; 0.00
    # 117 + 44 = 161
    # so this one can be decomposed into to categories.
    # If the number of parts is low, then it is likely not a good prefix.
    search = "https://www.weltderphysik.de/gebiet/te"
    for url, data in new_urls.items():
        if url.startswith(search):
            print("Candidate:", url, data['total'])

if __name__ == "__main__":
    main()