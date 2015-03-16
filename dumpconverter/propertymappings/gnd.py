property_mapping = {
    # Properties for Persons
    19: [
        {
            "nodes": [
                "ns:datafield[@tag='551' and ns:subfield[@code='i']='Geburtsort']/ns:subfield[@code='a']/text()"
            ]
        }
    ],
    20: [
        {
            "nodes": [
                "ns:datafield[@tag='551' and ns:subfield[@code='i']='Sterbeort']/ns:subfield[@code='a']/text()"
            ]
        }
    ],
    22: [
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Vater']/ns:subfield[@code='a']/text()"
            ],
            "formatter": "nodes[0].split(', ')[1] + ' ' + nodes[0].split(', ')[0]"
        },
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Vater']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Vater']/ns:subfield[@code='b']/text()"
            ],
            "formatter": "nodes[0] + ' ' + nodes[1]"
        }
    ],
    25: [
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Mutter']/ns:subfield[@code='a']/text()"
            ],
            "formatter": "nodes[0].split(', ')[1] + ' ' + nodes[0].split(', ')[0]"
        },
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Mutter']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Mutter']/ns:subfield[@code='b']/text()"
            ],
            "formatter": "nodes[0] + ' ' + nodes[1]"
        }
    ],
    26: [
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau']/ns:subfield[@code='a']/text()"
            ],
            "formatter": "nodes[0].split(', ')[1] + ' ' + nodes[0].split(', ')[0]"
        },
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau']/ns:subfield[@code='b']/text()"
            ],
            "formatter": "nodes[0] + ' ' + nodes[1]"
        }
    ],
    39: [
        {
            "nodes": [
                "/record/datafield[@tag='550' and subfield[@code='i']='Funktion']/subfield[@code='a']/text()"
            ]
        }
    ],
    40: [
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter']/ns:subfield[@code='a']/text()"
            ],
            "formatter": "nodes[0].split(', ')[1] + ' ' + nodes[0].split(', ')[0]"
        },
        {
            "nodes": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter']/ns:subfield[@code='b']/text()"
            ],
            "formatter": "nodes[0] + ' ' + nodes[1]"
        }
    ],
    106: [
        {
            "nodes": [
                "/record/datafield[@tag='550' and (subfield[@code='i']='Charakteristischer Beruf' or subfield[@code='i']='Beruf')]/subfield[@code='a']/text()"
            ]
        }
    ],
    410: [
        {
            "nodes": [
                "/record/datafield[@tag='550' and subfield[@code='i']='Funktion']/subfield[@code='a']/text()"
            ]
        }
    ],
    569: [
        {
            "nodes": [
                "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten']/ns:subfield[@code='a']/text()"
            ],
            "formatter": "nodes[0].split('-')[0]"
        }
    ],
    570: [
        {
            "nodes": [
                "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten']/ns:subfield[@code='a']/text()"
            ],
            "formatter": "nodes[0].split('-')[1]"
        }
    ],
    625: [
        {
            "nodes": [
                "ns:datafield[@tag='034' and ns:subfield[@code='9']='A:dgx']/ns:subfield[@code='d']/text()",
                "ns:datafield[@tag='034' and ns:subfield[@code='9']='A:dgx']/ns:subfield[@code='f']/text()"
            ],
            "formatter": "nodes[1] + ',' + nodes[0]"
        }
    ],

    # Geographical properties
    1477: [
        {
            "nodes": [
                "ns:datafield[@tag='400' and @ind1='1' and ns:subfield[@code='i']='Wirklicher Name']/ns:subfield[@code='a']/text()"
            ],
            "formatter": "nodes[0].split(', ')[1] + ' ' + nodes[0].split(', ')[0]"
        },
        {
            "nodes": [
                "ns:datafield[@tag='400' and @ind1='0' and ns:subfield[@code='i']='Wirklicher Name']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='400' and @ind1='0' and ns:subfield[@code='i']='Wirklicher Name']/ns:subfield[@code='b']/text()"
            ],
            "formatter": "nodes[0] + ' ' + nodes[1]"
        }
    ],
}