from json import loads, dumps
from functools import (
    partial
)
from lxml import etree

from fnc import (
    compose,
)

from xmltodict import ( # should this library be trusted?
    parse as xml_to_o_dict,
    unparse as dict_to_xml,
)

def assert_is_xml(xml: str) -> bool:
    etree.fromstring(xml)
    return xml

def assert_are_xml(*args) -> bool:
    return compose(
        (map, assert_is_xml),
        list,
        all
    )(args)

def merge(xml1: str, xml2: str) -> str:
    assert_are_xml(xml1, xml2)
    # TODO: consider using convert to json, merge, then normalize to do this
    x1, x2 = etree.fromstring(xml1), etree.fromstring(xml2)
    x1.extend(x2)
    return etree.tostring(x1)

def to_dict(xml: str) -> dict:
    return compose(
        assert_is_xml,
        # turn xml into an ordered dictionary
        xml_to_o_dict,
        # turn it into json and back to remove ordering
        partial(dumps, sort_keys=True),
        # sorted keys because when we unparse it we want it to be normalized
        loads
    )(xml)

def normalize(xml: str) -> str: #xml
    assert_is_xml(xml)
    return dict_to_xml(to_dict(xml))

def apply_hash(xml: str, hashing_function=None) -> str:
    assert_is_xml(xml)
    if not hashing_function:
        hashing_function = hash
    normalized_xml = normalize(xml)
    return hashing_function(normalized_xml)

def equals(xml1: str, xml2: str) -> bool:
    assert_are_xml(xml1, xml2)
    # we do this because we do NOT care about dict order
    d1, d2 = to_dict(xml1), to_dict(xml2)
    return d1 == d2



# from xmldiff.main import (
#     diff_texts
# )
# old method of equality testing, also kind of cool
# def equals(xml1, xml2) -> bool:
#     diffs: list = diff_texts(xml1, xml2)
#     # TODO: in the following
#     # ignore the following types from the list
#     # InsertComment - still equal even with comments
#     # MoveNode - we don't care about order
#     return not diffs