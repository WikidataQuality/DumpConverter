"""Contains property mapping from GND to Wikidata."""
from formatters.gnd import *


property_mapping = {
    # Properties for Persons
    19: [
        {
            "value_paths": [
                "ns:datafield[@tag='551' and ns:subfield[@code='i']='Geburtsort']/ns:subfield[@code='a']/text()"
            ]
        }
    ],
    20: [
        {
            "value_paths": [
                "ns:datafield[@tag='551' and ns:subfield[@code='i']='Sterbeort']/ns:subfield[@code='a']/text()"
            ]
        }
    ],
    21: [
        {
            "value_paths": [
                "ns:datafield[@tag='375']/ns:subfield[@code='a']/text()"
            ],
            "formatter": gender_formatter
        }
    ],
    22: [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Vater']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Vater']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Vater']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    25: [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Mutter']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Mutter']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Mutter']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    26: [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    39: [
        {
            "value_paths": [
                "ns:datafield[@tag='550' and subfield[@code='i']='Funktion']/subfield[@code='a']/text()"
            ]
        }
    ],
    40: [
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='1' and ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='500' and @ind1='0' and ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],
    106: [
        {
            "value_paths": [
                "ns:datafield[@tag='550' and (subfield[@code='i']='Charakteristischer Beruf' or subfield[@code='i']='Beruf')]/subfield[@code='a']/text()"
            ]
        }
    ],
    410: [
        {
            "value_paths": [
                "ns:datafield[@tag='550' and subfield[@code='i']='Funktion']/subfield[@code='a']/text()"
            ]
        }
    ],
    569: [
        {
            "value_paths": [
                "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten']/ns:subfield[@code='a']/text()"
            ],
            "formatter": start_date_formatter
        }
    ],
    570: [
        {
            "value_paths": [
                "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten']/ns:subfield[@code='a']/text()"
            ],
            "formatter": end_date_formatter
        }
    ],
    1477: [
        {
            "value_paths": [
                "ns:datafield[@tag='400' and @ind1='1' and ns:subfield[@code='i']='Wirklicher Name']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='400' and @ind1='0' and ns:subfield[@code='i']='Wirklicher Name']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='400' and @ind1='0' and ns:subfield[@code='i']='Wirklicher Name']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],

    # Properties for literary works
    50: [
        {
            "value_paths": [
                "ns:datafield[@tag='100' and @ind1='1']/ns:subfield[@code='a']/text()"
            ],
            "formatter": basic_name_formatter
        },
        {
            "value_paths": [
                "ns:datafield[@tag='100' and @ind1='0']/ns:subfield[@code='a']/text()",
                "ns:datafield[@tag='100' and @ind1='0']/ns:subfield[@code='b']/text()"
            ],
            "formatter": personal_name_formatter
        }
    ],

    # Geographical properties
    625: [
        {
            "value_paths": [
                "ns:datafield[@tag='034' and ns:subfield[@code='9']='A:dgx']/ns:subfield[@code='f']/text()",
                "ns:datafield[@tag='034' and ns:subfield[@code='9']='A:dgx']/ns:subfield[@code='d']/text()"
            ],
            "formatter": geo_coordinate_formatter
        }
    ]
}
