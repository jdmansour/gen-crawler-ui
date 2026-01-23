import json
from datetime import datetime
import requests

class FieldsProcessor:
    known_fields = [
        'cclom:title',
        'cclom:general_description',
        'ccm:wwwurl',
        'cclom:general_language',
        'ccm:published_date',
        'cm:created',
        'cm:modified',
        'cclom:version',
        'cclom:typicallearningtime',
        'cclom:duration',
        'ccm:curriculum',
        'ccm:educationalintendedenduserrole',
        'ccm:oeh_competence_requirements',
        'ccm:oeh_profession_group',
        'ccm:oeh_languageTarget',
        'ccm:oeh_languageLevel',
        'ccm:educationalcontext',
        'ccm:educationaltypicalagerange',
        'ccm:oeh_lrt',
        'ccm:taxonid',
        'cclom:general_keyword',
        'virtual:mediatype',
        'cclom:format',
        'license',
        'ccm:price',
        'ccm:oeh_quality_login',
    ]

    groups = [
        {
            'id': 'general',
            'display': 'Allgemein',
            'icon': 'description',
            'fields': [
                'cclom:title',
                'cclom:general_description',
                'ccm:wwwurl',
                'cclom:general_language',
                'ccm:published_date',
                'cm:created',
                'cclom:version',
                'cm:modified',
            ]
        },
        {
            'id': 'pedagogical',
            'display': 'Pädagogisches',
            'icon': 'school',
            'fields': [
                'cclom:typicallearningtime',
                'cclom:duration',
                'ccm:curriculum',
                'ccm:educationalintendedenduserrole',
                'ccm:oeh_competence_requirements',
                'ccm:oeh_profession_group',
                'ccm:oeh_languageTarget',
                'ccm:oeh_languageLevel',
            ]
        },
        {
            'id': 'typisierung',
            'display': 'Typisierung',
            'icon': 'done_all',
            'fields': [
                'ccm:oeh_lrt',
                'ccm:taxonid',
                'cclom:general_keyword',
                'ccm:educationalcontext',
                'ccm:educationaltypicalagerange',
                'virtual:mediatype',
                'cclom:format',
            ]
        },
        {
            'id': 'license',
            'display': 'Lizenz',
            'icon': 'copyright',
            'fields': [
                'license',
            ]
        },
        {
            'id': 'quality',
            'display': 'Zugänglichkeit / Qualität',
            'icon': 'accessibility',
            'fields': [
                'ccm:price',
                'ccm:oeh_quality_login',
            ]
        }
    ]

    inheritable_fields = [
        'cclom:general_language',
        'ccm:published_date',
        'cclom:typicallearningtime',
        'cclom:duration',
        'ccm:curriculum',
        'ccm:educationalintendedenduserrole',
        'ccm:oeh_competence_requirements',
        'ccm:oeh_profession_group',
        'ccm:oeh_languageTarget',
        'ccm:oeh_languageLevel',
        'ccm:educationalcontext',
        'ccm:educationaltypicalagerange',
        'cclom:format',
        'virtual:mediatype',
        'ccm:oeh_lrt',
        'ccm:taxonid',
        'cclom:general_keyword',
        'license',
        'ccm:price',
        'ccm:oeh_quality_login',
    ]
    
    recommended_fields = [
        'cclom:general_language',
        'ccm:published_date',
        'cclom:typicallearningtime',
        'cclom:duration',
        'ccm:curriculum',
        'ccm:educationalintendedenduserrole',
        'ccm:oeh_competence_requirements',
        'ccm:oeh_profession_group',
        'ccm:oeh_languageTarget',
        'ccm:oeh_languageLevel',
        'ccm:educationalcontext',
        'ccm:educationaltypicalagerange',
        'ccm:oeh_lrt',
        'ccm:taxonid',
        'cclom:general_keyword',
        'ccm:educationalcontext',
    ]


    def __init__(self):
        with open('data/mds_oeh.json', 'r', encoding='utf-8') as f:
            self.mds_oeh = json.load(f)

        with open('data/metadata.json', 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)

    # known field types:
    # text
    # textarea
    # multivalueFixedBadges
    # date

    # # general
    # field = 'cclom:title'
    # # field = 'cclom:general_description'
    # field = 'ccm:wwwurl'
    # # field = 'cclom:general_language'
    # field = 'ccm:published_date'

    # # Pädagogisches
    # field = 'cclom:typicallearningtime'
    # field = 'cclom:duration'
    # field = 'ccm:curriculum'
    # # Pädagogisches - Zielgruppe
    # field = 'ccm:educationalintendedenduserrole'
    # field = 'ccm:oeh_competence_requirements'
    # # diese beiden zusammen:
    # field = 'ccm:oeh_languageTarget'
    # # field = 'ccm:oeh_languageLevel'
    #     # field = 'ccm:educationalcontext'

    def process(self, guid: str):
        EDU_SHARING_BASE_URL = "https://repository.staging.openeduhub.net/edu-sharing"
        # GET {{EDU_SHARING_BASE_URL}}/rest/mds/v1/metadatasets/-home-/mds_oeh

        response = requests.get(f"{EDU_SHARING_BASE_URL}/rest/mds/v1/metadatasets/-home-/mds_oeh")
        self.mds_oeh = response.json()

        # get /node/v1/nodes/{repository}/{node}/metadata
        response = requests.get(f"{EDU_SHARING_BASE_URL}/rest/node/v1/nodes/-home-/{guid}/metadata", params={'propertyFilter': '-all-'})

        print("Metadata")
        print(response.text)
        self.metadata = response.json()

        result = {
            'fields': [self.get_field_obj(f) for f in self.known_fields],
            'groups': self.groups,
        }
        return result

    # field_obj = get_field_obj(metadata, mds_oeh, field)
    

    def get_field_obj(self, field):

        properties = self.metadata['node']['properties']
        values = properties.get(field, [])
        # print(values)

        # translate back using mds_oeh
        widgets = {w['id'].lower(): w for w in self.mds_oeh['widgets']}
        widget = widgets[field.lower()]
        field_type = widget['type']
        # print(widget)
        # field_values = []
        field_caption = widget['caption']
        field_bottomCaption = widget.get('bottomCaption', '')
        field_placeholder = widget.get('placeholder', '')
        #if widget.get('values') is not None:
        if field_type in ['multivalueFixedBadges', 'multivalueTree', 'multivalueSuggestBadges']:
            # multiple values, translate
            # this can be None in the JSON
            # TODO: do we want to differentiate between no value and empty value?
            field_values = []
            if widget_values := widget.get("values", None):
                # print("field:", field, "type:", field_type, "values:", widget_values, file=sys.stderr)
                values_by_id = {v['id']: v for v in widget_values}
                def get_display_dict(v):
                    res = {'value': v, 'display': values_by_id[v]['caption']}
                    if parent := values_by_id[v].get('parent', None):
                        res['parent'] = get_display_dict(parent)
                    return res
            
                field_values = [get_display_dict(v) for v in values if v in values_by_id]
            field_value = None
        elif field_type == 'singleoption':
            # expect single value, translate
            values_by_id = {v['id']: v for v in widget['values']}
            field_value = None
            if values and values[0] in values_by_id:
                v = values_by_id[values[0]]
                field_value = {'value': v['id'], 'display': v['caption']}
            field_values = None
        elif field_type == 'license':
            # ccm_commonlicense_key = properties.get('ccm:commonlicense_key', None)
            # ccm_commonlicense_cc_version = properties.get('ccm:commonlicense_cc_version', None)
            license_url = properties.get('virtual:licenseurl', None)
            license_icon = properties.get('virtual:licenseicon', None)

            field_value = {
                'url': license_url,
                'icon_url': license_icon,
                'cc_key': properties.get('ccm:commonlicense_key', None),
                'cc_version': properties.get('ccm:commonlicense_cc_version', None),
            }
            field_values = None
        elif field_type == 'range':
            from_field = f"{field}_from"
            to_field = f"{field}_to"
            from_value = properties.get(from_field, [])
            to_value = properties.get(to_field, [])
            from_value = from_value[0] if from_value else None
            to_value = to_value[0] if to_value else None
            if from_value and to_value:
                field_display = f'{from_value} - {to_value}'
            else:
                field_display = None
            field_value = {
                'from': from_value,
                'to': to_value,
                'display': field_display,
            }
            field_values = None
        elif field_type == 'duration':
            # duration is stored as seconds as a string
            if duration_msec := properties.get(field, None):
                duration_msec = int(duration_msec[0])
                # format as H:M:S or M:S
                hours = duration_msec // 3600000
                minutes = (duration_msec % 3600000) // 60000
                seconds = (duration_msec % 60000) // 1000
                if hours > 0:
                    display = f'{hours}:{minutes:02}:{seconds:02} h'
                else:
                    display = f'{minutes}:{seconds:02} min'

                field_value = {
                    'value': duration_msec,
                    'display': display,
                }
            else:
                field_value = None
            field_values = None

        elif field_type == 'date':

            key = f"{field}ISO8601"
            values = properties.get(key, [])
            if values and len(values) > 0:
                # example: "2024-01-24T12:10:21.583Z"
                # format date for german locale
                # 24. Januar 2024, 13:10

                display = datetime.fromisoformat(values[0].replace('Z', '+00:00')).strftime('%d.%m.%Y, %H:%M')
                field_value = {'value': values[0], 'display': display}
            else:
                field_value = None

            field_values = None
            
        else:
            # expect single value, no translation
            field_values = None
            field_value = values[0] if values else None

        field_obj = {
            'id': field,
            'type': field_type,
            'inheritable': field in self.inheritable_fields,
            'recommended': field in self.recommended_fields,
            'caption': field_caption,
            'bottomCaption': field_bottomCaption,
            'placeholder': field_placeholder,
        }

        if field_values is not None:
            field_obj['values'] = field_values
        else:
            field_obj['value'] = field_value
        return field_obj
