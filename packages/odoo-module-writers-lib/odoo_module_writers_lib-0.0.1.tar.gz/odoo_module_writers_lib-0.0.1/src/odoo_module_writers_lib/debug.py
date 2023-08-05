# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: João Jerónimo (joao.jeronimo.pro@gmail.com)
#    Copyright (C) 2019-2022 - Licensed under the terms of GNU LGPL
#
##############################################################################

from odoo import models, fields, api, tools, SUPERUSER_ID
import sqlparse, re

def concat_nums(sqlcode):
    pattern = "^( +)([0-9]+),\n"
    tosubto = " \\2,"
    #pdb.set_trace()
    return re.sub(pattern, tosubto, sqlcode, count=0, flags=re.MULTILINE )

def separate_n_nums(sqlcode, n):
    pattern = "^" + "("+ (" [0-9]+,"*n) + ")"+" "
    tosubto = "\\1\n "
    #pdb.set_trace()
    while re.search(pattern, sqlcode, flags=re.MULTILINE):
        sqlcode = re.sub(pattern, tosubto, sqlcode, count=0, flags=re.MULTILINE )
    return sqlcode

def indent_ANDs(sqlcode):
    pattern = "^( +)(AND) +([^\n]+)\n"
    tosubto = '\\1\\2\n\\1\\3\n'
    #pdb.set_trace()
    return re.sub(pattern, tosubto, sqlcode, count=0, flags=re.MULTILINE )

def indent_open_pars(sqlcode):
    pattern = "^( +)\(\("
    tosubto = '\\1(\n\\1 ('
    #pdb.set_trace()
    while re.search(pattern, sqlcode, flags=re.MULTILINE):
        sqlcode = re.sub(pattern, tosubto, sqlcode, count=0, flags=re.MULTILINE )
    return sqlcode

def indent_close_pars(sqlcode):
    ### This operation was commented because it's context-free, not regex:
    #pattern = "^( +) ([^\n]+)\)\)$"
    #tosubto = '\\1 \\2)\n\\1)'
    ##pdb.set_trace()
    #while re.search(pattern, sqlcode, flags=re.MULTILINE):
    #    sqlcode = re.sub(pattern, tosubto, sqlcode, count=0, flags=re.MULTILINE )
    return sqlcode

def repr_strs(fmtlist):
    ret = tuple([
        repr(fmt) if isinstance(fmt, str) else str(fmt)
        for fmt in fmtlist ])
    #pdb.set_trace()
    return ret

def build_pretty_title(full_text):
    BORDER_CHARS = 5
    full_text_lins = [ lin.strip()
            for lin
            in full_text.split('\n')
            if len(lin.strip()) > 0             ]
    # Calculate drawing vars for heading:
    max_line_len = max([ len(l) for l in full_text_lins ])
    top_bottom_signs = max_line_len + (BORDER_CHARS+1)*2
    # Build heading according to calculated values:
    ret = ""
    ret += ( "="*top_bottom_signs + "\n")
    for thisLine in full_text_lins:
        ret += (( ( ("="*BORDER_CHARS)+" %-*s " + ("="*BORDER_CHARS) )
                    %(max_line_len, thisLine) ) + "\n")
    ret += ( "="*top_bottom_signs + "\n")
    return ret


def sql_prettyfy(log_label, sql_query):
    pretty = sqlparse.format(
        sql_query,
        reindent=True,
        keyword_case='upper',
        wrap_after=120,
        #indent_after_first=True,
        )
    pretty = indent_ANDs(pretty)
    pretty = indent_open_pars(pretty)
    pretty = indent_close_pars(pretty)
    # Build string to print:
    ret = build_pretty_title("SQL Log (%s)"%log_label)
    #BORDER_WIDTH = 5
    #ret = "\n"
    #ret += ("="*() + "\n")
    #ret += ("="*() + log_label + "="*() + "\n")
    #ret += ("="*() + "\n")
    return ret+pretty
