# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: João Jerónimo (joao.jeronimo.pro@gmail.com)
#    Copyright (C) 2019-2022 - Licensed under the terms of GNU LGPL
#
##############################################################################

import odoo
from odoo import api, fields, models

class SqlInheritedModel:
    def _sql_table_already_inherits(self, child, parent):
        esse_ke_elle_codez = ("""
                SELECT pg_inherits.*, childtab.relname AS child, partab.relname AS parent
                    FROM pg_inherits
                            INNER JOIN pg_class AS childtab ON (pg_inherits.inhrelid=childtab.oid)
                            INNER JOIN pg_class AS partab ON (pg_inherits.inhparent=partab.oid)
                    WHERE childtab.relname='%(child)s' AND partab.relname='%(parent)s';
            """ % {
            'child':    child,
            'parent':   parent,
            })
        self.env.cr.execute(esse_ke_elle_codez)
        halls = self.env.cr.fetchall()
        if len(list(halls)) == 0:
            return False
        else:
            return True
    def _sql_table_inherit(self, child, parent):
        self.env.cr.execute("ALTER TABLE %(child)s INHERIT %(parent)s;" % {
            'child':    child,
            'parent':    parent,
            })
    def _apply_sql_inheritance(self, mothertable):
        tabname = self._table
        #mothertable = self.env[self._inherit]._table
        if not self._sql_table_already_inherits(tabname, mothertable):
            self._sql_table_inherit(tabname, mothertable)

class ServerSideOnchangeMixin:
    def _collect_explicit_fields(self, vals, fields_and_methods):
        """
        vals                Dictionary of the kind often passed to create() and write().
        fields_and_methods  List of dictionaries in the form: [
                    { 'depends': "membership_situation_id", 'calls': "_onchange_membership_situation_id", 'sets': "pricelist_id" },
                    ]
        : returns   List of names of method that ought to be called after create() ou write().
        """
        explicit_fields = vals.keys()
        all_tocall = []
        for fieldspec in fields_and_methods:
            if fieldspec['depends'] in explicit_fields and fieldspec['sets'] not in explicit_fields:
                all_tocall.append(fieldspec['calls'])
        return all_tocall
    def _callall(selves, halls):
        """
        halls   A list of method names to call over self.
        """
        for self in selves:
            for tocall in halls:
                getattr(self, tocall)()
    
    def _callcreate_and_onchange(self, supermethod, vals, fields_and_methods):
        all_tocall = self._collect_explicit_fields(vals, fields_and_methods)
        supered_record = supermethod(vals)
        supered_record._callall(all_tocall)
        return supered_record
    def _callwrite_and_onchange(self, supermethod, vals, fields_and_methods):
        all_tocall = self._collect_explicit_fields(vals, fields_and_methods)
        supered_record = supermethod(vals)
        self._callall(all_tocall)
        return supered_record
