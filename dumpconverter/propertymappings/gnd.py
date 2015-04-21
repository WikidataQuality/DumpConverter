"""Contains property mapping from GND to Wikidata."""
from formatters.gnd import *


property_mapping = {
    # Properties for Persons (Tpgesamt)
    'P19': [
        {
            "value_paths": [
                "ns:datafield[@tag='551' and ns:subfield[@code='i']='Geburtsort' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ]
        }
    ],
    'P20': [
        {
            "value_paths": [
                "ns:datafield[@tag='551' and ns:subfield[@code='i']='Sterbeort' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ]
        }
    ],
    'P21': [
        {
            "value_paths": [
                "ns:datafield[@tag='375' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": gender_formatter
        }
    ],
    'P22': [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Vater' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Vater' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Vater' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    'P25': [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Mutter' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Mutter' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Mutter' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    'P26': [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and (ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau') and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and (ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau') and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and (ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau') and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    'P39': [
        {
            "value_paths": [
                "ns:datafield[@tag='550' and subfield[@code='i']='Funktion' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/subfield[@code='a']/text()"
            ]
        }
    ],
    'P40': [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and (ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter') and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and (ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter') and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and (ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter') and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    'P106': [
        {
            "value_paths": [
                "ns:datafield[@tag='550' and (subfield[@code='i']='Charakteristischer Beruf' or subfield[@code='i']='Beruf') and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/subfield[@code='a']/text()"
            ]
        }
    ],
    'P410': [
        {
            "value_paths": [
                "ns:datafield[@tag='550' and subfield[@code='i']='Funktion' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/subfield[@code='a']/text()"
            ]
        }
    ],
    'P569': [
        {
            "value_paths": [
                "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": start_date_formatter
        }
    ],
    'P570': [
        {
            "value_paths": [
                "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": end_date_formatter
        }
    ],
    'P1477': [
        {
            "value_paths": [
                "ns:datafield[@tag='400' and @ind1='1' and ns:subfield[@code='i']='Wirklicher Name' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='400' and @ind1='0' and ns:subfield[@code='i']='Wirklicher Name' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='400' and @ind1='0' and ns:subfield[@code='i']='Wirklicher Name' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='p']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],

    # Properties for literary works (Tugesamt)
    'P50': [
        {
            "value_paths": [
                "ns:datafield[@tag='100' and @ind1='1' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='s']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='100' and @ind1='0' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='s']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='100' and @ind1='0' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='s']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],

    # Geographical properties (Tggesamt)
    'P625': [
        {
            "value_paths": [
                "ns:datafield[@tag='034' and ns:subfield[@code='9']='A:dgx' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='g']/ns:subfield[@code='f']/text()",
                "ns:datafield[@tag='034' and ns:subfield[@code='9']='A:dgx' and //ns:datafield[@tag='079']/ns:subfield[@code='b']='g']/ns:subfield[@code='d']/text()"
            ],
            "formatter": geo_coordinate_formatter
        }
    ]
}
