# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: João Jerónimo (joao.jeronimo.pro@gmail.com)
#    Copyright (C) 2019-2022 - Licensed under the terms of GNU LGPL
#
##############################################################################

from odoo import models, fields, api, tools
from decorator import decorator




def aggregate(method, value, self):
    """ Aggregate record-style ``value`` for a method decorated with ``@one``. """
    spec = getattr(method, '_returns', None)
    if spec:
        # value is a list of instances, concatenate them
        model, _, _ = spec
        if model == 'self':
            return sum(value, self.browse())
        elif model:
            return sum(value, self.env[model])
    return value

def one(method):
    """ Decorate a record-style method where ``self`` is expected to be a
        singleton instance. The decorated method automatically loops on records,
        and makes a list with the results. In case the method is decorated with
        :func:`returns`, it concatenates the resulting instances. Such a
        method::
            @api.one
            def method(self, args):
                return self.name
        may be called in both record and traditional styles, like::
            # recs = model.browse(cr, uid, ids, context)
            names = recs.method(args)
            names = model.method(cr, uid, ids, args, context=context)
        .. deprecated:: 9.0
            :func:`~.one` often makes the code less clear and behaves in ways
            developers and readers may not expect.
            It is strongly recommended to use :func:`~.multi` and either
            iterate on the ``self`` recordset or ensure that the recordset
            is a single record with :meth:`~odoo.models.Model.ensure_one`.
    """
    def loop(method, self, *args, **kwargs):
        result = [method(rec, *args, **kwargs) for rec in self]
        return aggregate(method, result, self)

    wrapper = decorator(loop, method)
    wrapper._api = 'one'
    return wrapper
