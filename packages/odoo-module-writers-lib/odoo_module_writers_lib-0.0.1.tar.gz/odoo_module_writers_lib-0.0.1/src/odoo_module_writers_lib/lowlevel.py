# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: João Jerónimo (joao.jeronimo.pro@gmail.com)
#    Copyright (C) 2019-2022 - Licensed under the terms of GNU LGPL
#
##############################################################################

from odoo import models, fields, api, tools, SUPERUSER_ID

def Env(cr, modelname=False):
    ret = api.Environment(cr, SUPERUSER_ID, {})
    if modelname:
        ret = ret[modelname]
    return ret

############################################################################
### External IDs manipulation: #############################################
############################################################################
# Glossary:
#  A xid is a pair {'module: ???, 'name': ???}
#  A dxid is a string module.name

### Functions that get from modelname+id --> xid:
def get_xid(env, modelname, res_id):
    the_xid_record = env["ir.model.data"].search_read([
                    ('model',   '=', modelname),
                    ('res_id',  '=', res_id),
                    ], fields=['module', 'name'], limit=1)
    #print (str(the_xid_record))
    if len(the_xid_record)==1:  return the_xid_record[0]
    else:                       return False

## Functions that modify the (d)XIDs:
def assign_xid(env, xid_module, xid_name, modelname, res_id):
    write_dikt = {
        'module'    : xid_module,
        'name'      : xid_name,
        'model'     : modelname,
        'res_id'    : res_id,
        }
    # Now patch or create the record:
    existing_xid = get_xid(env, modelname, res_id)
    if existing_xid:
        env["ir.model.data"].browse(existing_xid['id']).write(write_dikt)
    else:
        env["ir.model.data"].create(write_dikt)
def assign_dxid(env, dxid, modelname, res_id):
    xid_module, xid_name = dxid.split('.')
    return assign_xid(env, xid_module, xid_name, modelname, res_id)

## High level functions:
def obj2dxid(env, obj):
    #pdb.set_trace()
    modelname = obj._name
    res_id = obj.id
    resulting_xid = get_xid(env, modelname, res_id)
    if resulting_xid:
        return ("%(module)s.%(name)s" % resulting_xid)
    else:
        return False
def assign_dxid_to_obj(env, obj, dxid):
    #pdb.set_trace()
    assign_dxid(env, dxid, obj._name, obj.id)

def merge_obj_to_module(env, srcmod, dstmod, xidname):
    src_dxid = "%s.%s" % (srcmod, xidname)
    dst_dxid = "%s.%s" % (dstmod, xidname)
    the_obj = env.ref(src_dxid, False)
    if not the_obj:
        return False
    assign_dxid_to_obj(env, the_obj, dst_dxid)
    return True

## Unlink and other operations:
def unlink_by_dxid(env, dxid):
    obj = env.ref(dxid, False)
    if obj: obj.unlink()

def unlink_dependants_views(env, parent_module_name, model_name):
    """
    Every view over model_name that is declared by dependants of parent_module_name is unlinked.
    """
    # Get every dependant of passed module name:
    every_dependant_name = get_all_module_dependants_by_name(env, parent_module_name)
    # Get every view res_id belonging to these modules:
    every_relevant_xid = env["ir.model.data"].search([
        ('module',  'in',   every_dependant_name),
        ('model',   '=',    "ir.ui.view"),
        ])
    # Get every that is over model_name AND was declared by one of these modules:
    views_to_unlink = env["ir.ui.view"].search([
        ('model',   '=',    model_name),
        ('id',      'in',   every_relevant_xid.mapped('res_id')),
        ])
    # Print information:
    print("== Deleting views:\n%s" % (
        "\n".join(views_to_unlink.mapped('xml_id')),
        ))
    # Do delete them:
    views_to_unlink.unlink()

def set_xid_to_updateable(env, dxid, strict=False):
    xid_module, xid_name = dxid.split('.')
    the_xid_record = env["ir.model.data"].search([
        ('module',  '=', xid_module),
        ('name',    '=', xid_name),
        ], limit=1)
    if not strict and len(the_xid_record)==0:
        return
    the_xid_record.noupdate = False

##########################################################################
### Module graph navigation: #############################################
##########################################################################
def get_module_by_name(env, mod_name):
    return env["ir.module.module"].search([
        ('name', '=', mod_name),
        ])

def get_module_direct_dependants(env, rs_mods):
    """
    Module dependants are other modules that depend on this module.
    This function returns direct dependants.
    """
    EnvModuleDependency = env["ir.module.module.dependency"]
    # Get every dependency object that points to this module:
    dependants = EnvModuleDependency.search([
        ('depend_id', 'in', rs_mods.ids),
        ]).mapped('module_id')
    #pdb.set_trace()
    return dependants

def get_all_module_dependants(env, rs_mods):
    """
    This function returns every direct and inderect dependants.
    """
    all_dependants = env["ir.module.module"]
    # Create rs the initially has the requested modules:
    current_mods = rs_mods
    # Adds their dependencies to the rs until the list is empty:
    while len(current_mods) > 0:
        # Get dependents of current module set:
        current_mods = get_module_direct_dependants(env, current_mods)
        # Adds them the the accomulator list:
        all_dependants += current_mods
    return all_dependants

def get_all_module_dependants_by_name(env, mod_name):
    """
    Return names of all modules that depend on module named mod_name.
    """
    return get_all_module_dependants(
        env,
        get_module_by_name(env, mod_name)
        ).mapped('name')
