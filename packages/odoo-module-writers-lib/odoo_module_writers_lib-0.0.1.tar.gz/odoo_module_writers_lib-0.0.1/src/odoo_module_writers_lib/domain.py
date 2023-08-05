# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: João Jerónimo (joao.jeronimo.pro@gmail.com)
#    Copyright (C) 2019-2022 - Licensed under the terms of GNU LGPL
#
##############################################################################

import math, logging
from datetime import datetime
from odoo import models, fields, api
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
_logger = logging.getLogger(__name__)


def term_filters_on_fieldnames(term_or_operator, fieldnames):
    if not isinstance(term_or_operator, (list, tuple)):
        return False
    assert len(term_or_operator)==3
    # Test the field names:
    if term_or_operator[0] in fieldnames:
        return True
    else:
        return False

def term_filters_on_values(term_or_operator, values):
    if not isinstance(term_or_operator, (list, tuple)):
        return False
    assert len(term_or_operator)==3
    # Test the field values:
    if isinstance(term_or_operator[2], (list, tuple)):
        return any((item in values) for item in term_or_operator[2])
    else:
        return term_or_operator[2] in values

#####################################################
##### Helpers for writing computer methods: #########
#####################################################
# Strings for building function names to call for each operator. Primiry operator are those
# that provide a full search() implementation for a given field; other operators' implmenetation
# can be systematically infered from those implementations. Leave unimplemented those that you
# want to raise an error.
OPERATOR_NAMES = {
    '=':            'EQUAL',            # Is primary.
    '!=':           'NOT_EQUAL',
    '<=':           'LTE',              # Is primary.
    '<':            'LT',
    '>':            'GT',
    '>=':           'GTE',              # Is primary.
    '=?':           'EQUAL_OR_NULL',
    '=like':        'FULL_LIKE',        # Is primary.
    '=ilike':       'FULL_ILIKE',       # Is primary.
    'like':         'LIKE',
    'not like':     'NOT_LIKE',
    'ilike':        'ILIKE',
    'not ilike':    'NOT_ILIKE',
    'in':           'IN',
    'not in':       'NOT_IN',
    'child_of':     'CHILD_OF',         # Is primary.
    'parent_of':    'PARENT_OF',        # Is primary.
    }

def raw_search_trampoline(caller_name, rs, operator, value):
    if operator in OPERATOR_NAMES.keys():
        method_name = '%s_%s' % (caller_name, OPERATOR_NAMES[operator], )
        method_object = getattr(rs, method_name, False)
        if method_object:
            return method_object(value)
    else:
        return False

def _search_trampoline(field_name, caller_name, rs, operator, value):
    #TERM_OPERATORS = ('=', '!=', '<=', '<', '>', '>=', '=?', '=like', '=ilike',
    #          'like', 'not like', 'ilike', 'not ilike', 'in', 'not in',
    #          'child_of', 'parent_of')
    
    # Note: this is to use for non-store computed fields, which means that no
    # operator ir defined to begin with. So, every operator must be translated
    # to a raw domain!
    
    # See if the operator is implemented - This is always used if implemented, as a way to write accelerators:
    implemented_result = raw_search_trampoline(caller_name, rs, operator, value)
    if implemented_result:
        return implemented_result
    # Otherwise, see if converse operator is implemented:
    term_operators_negation = {
        **expression.TERM_OPERATORS_NEGATION,
        **{ '=like':        'not =like',
            '=ilike':       'not =ilike',
            'not =like':    '=like',
            'not =ilike':   '=ilike',
            },
        }
    implemented_result = raw_search_trampoline(caller_name, rs, term_operators_negation[operator], value)
    if implemented_result:
        return ['!'] + implemented_result
    ### Some operator can also be translated into others:
    # Try to convert 'in' into a disjunction of equals:
    if operator == 'in':
        return expression.OR([
            expression.normalize_domain(raw_search_trampoline(caller_name, rs, '=', single_val))
            for single_val in value
            ])
    # Try to convert 'like', and 'ilike' into their full like equivalents:
    if operator == 'like': return search_trampoline(field_name, caller_name, rs, '=like', '%'+value+'%')
    if operator == 'not like': return search_trampoline(field_name, caller_name, rs, 'not =like', '%'+value+'%')
    if operator == 'ilike': return search_trampoline(field_name, caller_name, rs, '=ilike', '%'+value+'%')
    if operator == 'not ilike': return search_trampoline(field_name, caller_name, rs, 'not =ilike', '%'+value+'%')
    # If none if above mentioned deravation method worked, raise an error:
    raise UserError(_("Searching %s using operator %s is not impelemented.") % (field_name, operator,))

def search_trampoline(field_name, caller_name, rs, operator, value):
    """
    # Call this function like this:
    
    display_name = fields.Char((...), search="_search_display_name")
    
    def _search_display_name(self, operator, value):
        return omwl.domain.search_trampoline("display_name", "_search_display_name", self, operator, value)
    #(...)
    def _search_display_name_islike(self, value, case_sensitive=True):
        "Translates a domain term that looks like: ('display_name', '=like', value)"
        pass
    def _search_display_name_FULL_ILIKE(self, value):   return self._search_display_name_islike(value, case_sensitive=False)
    def _search_display_name_FULL_LIKE(self, value):    return self._search_display_name_islike(value, case_sensitive=True)
    
    """
    ret = _search_trampoline(field_name, caller_name, rs, operator, value)
    _logger.info("ORM domain «%(srcclause)s» translated into «%(dstdom)s»." % {
        'srcclause' : "(%s, %s, %s)" % (repr(field_name), repr(operator), repr(value), ),
        'dstdom'    : str(ret),
        })
    return ret
