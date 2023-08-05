# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: João Jerónimo (joao.jeronimo.pro@gmail.com)
#    Copyright (C) 2019-2022 - Licensed under the terms of GNU LGPL
#
##############################################################################

import math
from datetime import datetime
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

###############################
### Non-date stuff: ###########
###############################
def constrain(x, a, b):
    if x<a:
        return a
    elif x>b:
        return b
    else:
        return x

def concat_lists(thelists):
    return sum(thelists, [])

def transform_dictionary_keys(dictionary, func):
    return dict([
        (func(it1), it2)
        for it1, it2 in dictionary.items()
        ])

def is_subdictionary(superdictionary, subdictionary):
    """
    Returns true if subdictionary if a subdistionary of superdictionary, that is,
    if all keys of subdictionary have the same values as the keys of
    superdictionary with the same names.
    Object superdictionary may have more information than subdictionary, and we
    need that information.
        superdictionary     A dict object.
        subdictionary       Another dict object.
    """
    def key_matches(oned, otherd, key):
        uneval = oned[key]
        otherval = otherd[key]
        return uneval == otherval
    return all([
        key_matches(superdictionary, subdictionary, key)
        for key in subdictionary.keys()
        ])

def filter_subdictionaries(select_results, one_subresult):
    """
    Given a list of dictionaries 'select_results', returns another list of every
    element that is a superdictionary of one_subresult.
        select_results      A list of dict objects.
        one_pk              A dict object - contains a subset of the keys of each of
                            the select_results elements.
    Returns: List of elements of select_results whose keys that they have in
             common with one_subresult are all equal.
    """
    return [
        res for res in select_results
        if is_subdictionary(res, one_subresult)
        ]

def filter_dictionary_by_keys(dictionary, keys):
    """
    Given a dictionary, returns another one that only contains the keys listed in keys.
        dictionary      A dict object.
        keys            A list object.
    """
    return dict([
        dtuple
        for dtuple in list( dictionary.items() )
        if dtuple[0] in keys
        ])

def filter_dictionaries_by_keys(dictionaries, keys):
    """
    Given a list of dictionaries, apply filter_dictionary_by_keys to every dictionary on it.
    """
    return [
        filter_dictionary_by_keys(thedict, keys)
        for thedict in dictionaries
        ]

def invert_dictionary(ori_dict):
    return {v: k for k, v in ori_dict.items()}
