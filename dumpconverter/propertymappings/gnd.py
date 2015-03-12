property_mapping = {
    19: {
        "nodeSelector": "ns:datafield[@tag='551' and ns:subfield[@code='i']='Geburtsort']/ns:subfield[@code='a']/text()"
        },
    20: {
        "nodeSelector": "ns:datafield[@tag='551' and ns:subfield[@code='i']='Sterbeort']/ns:subfield[@code='a']/text()"
        },
    22: {
        "nodeSelector": "ns:datafield[@tag='500' and ns:subfield[@code='9']='v:Vater']/ns:subfield[@code='a']",
        "valueFormatter": "concat(substring-after(./text(), ', '), ' ', substring-before(./text(), ', '))"
        },
    25: {
        "nodeSelector": "ns:datafield[@tag='500' and ns:subfield[@code='9']='v:Mutter']/ns:subfield[@code='a']",
        "valueFormatter": "concat(substring-after(./text(), ', '), ' ', substring-before(./text(), ', '))"
        },
    26: {
        "nodeSelector": "ns:datafield[@tag='500' and ns:subfield[@code='9']='v:Ehemann' or ns:subfield[@code='9']='v:Ehefrau']/ns:subfield[@code='a']",
        "valueFormatter": "concat(substring-after(./text(), ', '), ' ', substring-before(./text(), ', '))"
        },
    40: {
        "nodeSelector": "ns:datafield[@tag='500' and ns:subfield[@code='9']='v:Sohn' or ns:subfield[@code='9']='v:Tochter']/ns:subfield[@code='a']",
        "valueFormatter": "concat(substring-after(./text(), ', '), ' ', substring-before(./text(), ', '))"
        },
    569: {
        "nodeSelector": "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten']/ns:subfield[@code='a']",
        "valueFormatter": "substring-before(./text(), '-')"
        },
    570: {
        "nodeSelector": "ns:datafield[@tag='548' and ns:subfield[@code='i']='Exakte Lebensdaten']/ns:subfield[@code='a']",
        "valueFormatter": "substring-after(./text(), '-')"
        },
    625: {
        "nodeSelector": "ns:datafield[@tag='034' and ns:subfield[@code='9']='A:dgx']/ns:subfield[@code='d']",
        },
    1477: {
        "nodeSelector": "ns:datafield[@tag='400' and ns:subfield[@code='i']='Wirklicher Name']/ns:subfield[@code='a']",
        "valueFormatter": "concat(substring-after(./text(), ', '), ' ', substring-before(./text(), ', '))"
    }
}