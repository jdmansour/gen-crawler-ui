import json

def main():
    filename = "bread.jsonlines"
    tree = {}
    with open(filename, "r") as f:
        for line in f:
            obj = json.loads(line)
            breadcrumbs = obj.get("breadcrumbs", [])
            put_in_tree(tree, breadcrumbs)
    print(json.dumps(tree, indent=2))
    
# Example object:
# {"job_id": null, "url": "https://o-mathe.de/differentialrechnung/anwendungen/optimierungsprobleme/spielfeld/lernstrecke/problemversion2", "breadcrumbs_found": true, "breadcrumb_selector": "nav.breadcrumbs", "breadcrumb_item_selector": "a.breadcrumb:not(:first-child)", "breadcrumbs": [{"name": "Startseite", "url": "https://o-mathe.de/"}, {"name": "Differentialrechnung", "url": "https://o-mathe.de/differentialrechnung"}, {"name": "Anwendungen von Funktionsuntersuchungen", "url": "https://o-mathe.de/differentialrechnung/anwendungen"}, {"name": "Optimierungsprobleme", "url": "https://o-mathe.de/differentialrechnung/anwendungen/optimierungsprobleme"}, {"name": "Fallstudie – Optimales Spielfeld", "url": "https://o-mathe.de/differentialrechnung/anwendungen/optimierungsprobleme/spielfeld"}, {"name": "Die Ausgangssituation", "url": "https://o-mathe.de/differentialrechnung/anwendungen/optimierungsprobleme/spielfeld/lernstrecke"}, {"name": "Das Optimierungsproblem – Version 2", "url": "https://o-mathe.de/differentialrechnung/anwendungen/optimierungsprobleme/spielfeld/lernstrecke/problemversion2"}]}

def put_in_tree(tree, breadcrumbs):
    if not breadcrumbs:
        return
    breadcrumb = breadcrumbs[0]
    name = breadcrumb["name"]
    url = breadcrumb["url"]
    if name not in tree:
        tree[name] = {"url": url, "children": {}}
    put_in_tree(tree[name]["children"], breadcrumbs[1:])

if __name__ == "__main__":
    main()