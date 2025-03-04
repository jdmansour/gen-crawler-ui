import logging
import re

import requests

log = logging.getLogger(__name__)

class Valuespaces:
    idsVocabs = [
        "conditionsOfAccess",
        "discipline",
        "educationalContext",
        "hochschulfaechersystematik",
        "intendedEndUserRole",
        "languageLevel",
        "learningResourceType",
        "new_lrt",
        "oer",
        "sourceContentType",
        "toolCategory",
    ]
    idsW3ID = ["containsAdvertisement", "price", "accessibilitySummary", "dataProtectionConformity", "fskRating"]
    data = {}

    def __init__(self):
        vocab_list: list[dict] = []
        # one singular dictionary in the vocab list will typically look like this:
        # {'key': 'discipline', 'url': 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/discipline/index.json'}
        for v in self.idsVocabs:
            vocab_list.append(
                {"key": v, "url": "https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/" + v + "/index.json"}
            )
        for v in self.idsW3ID:
            vocab_list.append({"key": v, "url": "http://w3id.org/openeduhub/vocabs/" + v + "/index.json"})
        for vocab_name in vocab_list:
            # try:
            r = requests.get(vocab_name["url"])
            self.data[vocab_name["key"]] = self.flatten(r.json()["hasTopConcept"])
            # except:
            #    self.valuespaces[v] = {}

    def flatten(self, tree: []):
        result = tree
        for leaf in tree:
            if "narrower" in leaf:
                result.extend(self.flatten(leaf["narrower"]))
        return result

    @staticmethod
    def findKey(valuespaceId: str, id: str, valuespace=None):
        if not valuespace:
            valuespace = Valuespaces.data[valuespaceId]
        for key in valuespace:
            if key["id"] == id:
                return key
            if "narrower" in key:
                found = Valuespaces.findKey(valuespaceId, id, key["narrower"])
                if found:
                    return found
        return None

    def findInText(self, valuespaceId: str, text: str, valuespace = None) -> list[str]:
        if valuespace is None:
            valuespace: list[dict] = self.data[valuespaceId]

        result: set[str] = set()
        for v in valuespace:
            # Example:
            # {'id': 'http://w3id.org/openeduhub/vocabs/discipline/220',
            #  'prefLabel': {'de': 'Geografie', 'en': 'Geography'},
            #  'altLabel': {'de': ['Erdkunde', 'Geographie']}}
            labels = list(v["prefLabel"].values())
            alt_labels = v.get("altLabel", {})
            for tmp in alt_labels.values():
                if isinstance(tmp, list):
                    labels.extend(tmp)
                elif isinstance(tmp, str):
                    labels.append(tmp)

            labels = list(map(lambda x: x.casefold(), labels))
            for label in labels:
                if re.search(r"\b" + label + r"\b", text.casefold()):
                    result.add(v["id"])
                    break

            if 'narrower' in v:
                result.update(self.findInText(valuespaceId, text, v['narrower']))

        return list(result)

    def initTree(self, tree):
        for t in tree:
            names = self.getNames(t)
            # t['words'] = list(map(lambda x: nlp(x)[0], names))
            t["words"] = names
            if "narrower" in t:
                self.initTree(t["narrower"])

    def getNames(self, key):
        names = []
        if "prefLabel" in key:
            if "de" in key["prefLabel"]:
                names += [key["prefLabel"]["de"]]
            if "en" in key["prefLabel"]:
                names += [key["prefLabel"]["en"]]
        if "altLabel" in key:
            names += key["altLabel"]["de"] if "de" in key["altLabel"] else []
            names += key["altLabel"]["en"] if "en" in key["altLabel"] else []
        if "note" in key:
            names += key["note"]["de"] if "de" in key["note"] else []
            names += key["note"]["en"] if "en" in key["note"] else []

        names = list(set(map(lambda x: x.strip(), names)))
        return names
