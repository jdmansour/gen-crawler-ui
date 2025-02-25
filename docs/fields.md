
Fields of the generic crawler

| JSON field                      | edu-sharing                        | source                                 |
| ------------------------------- | ---------------------------------- | -------------------------------------- |
| *spider name*                   | ccm:replicationsource              |                                        |
| sourceId                        | ccm:replicationsourceid            |                                        |
| hash                            | ccm:replicationsourcehash          |                                        |
| thumbnail                       | ?                                  | JSON-LD, OpenGraph                     |
| -                               | ccm:replicationsourceuuid          |                                        |
| ai_prompts                      | -                                  |                                        |
| kidra_raw/curriculum            | ccm:curriculum                     | KI                                     |
| kidra_raw/text_difficulty       | ccm:oeh_text_difficulty            | KI                                     |
| kidra_raw/text_reading_time     | ccm:oeh_text_reading_time          | KI                                     |
| kidra_raw/kidra_disciplines     | -                                  | KI                                     |
| lom/general/title               | cc:name, cclom:title               | OpenGraph, HTML5                       |
| lom/general/language            | cclom:general_language             | JSON-LD, HTML5                         |
| lom/general/description         | cclom:general_description          | JSON-LD (description, about), KI (LLM) |
| lom/general/keyword             | cclom:general_keyword              | JSON-LD, KI (LLM)                      |
| lom/educational                 | -                                  |                                        |
| lom/classification              | -                                  |                                        |
| lom/technical/format            | cclom:format                       |                                        |
| lom/technical/location          | cclom:location                     |                                        |
| lom/technical/size              | -                                  |                                        |
| license/url                     | *(transformed)*                    | HTML, Trafilatura                      |
| -                               | ccm:commonlicense_key,             |                                        |
| -                               | ccm:commonlicense_cc_version       |                                        |
| license/author                  |                                    | HTML                                   |
| valuespaces/discipline          | ccm:taxonid                        | KI (LLM)                               |
| valuespaces/educationalContext  | ccm:educationalcontext             | KI (LLM)                               |
| valuespaces/intendedEndUserRole | ccm:educationalintendedenduserrole | KI (LLM)                               |
| valuespaces/new_lrt             | ccm:oeh_lrt                        | KI (LLM)                               |
| permissions                     | ?                                  |                                        |
| response                        | ?                                  |                                        |
