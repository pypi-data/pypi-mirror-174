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
#import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
#import logging
#_logger = logging.getLogger(__name__)
import pdb

############
### Aux function for dates and times:
############
def month_1st_day(thedate):
    if type(thedate)==str:
        thedate = castdate(thedate)
    return castdate(("%d-%02d-%02d" % (thedate.year, thedate.month, 1, )))
def month_last_day(thedate):
    return addmonths(month_1st_day(thedate), 1) + relativedelta(days = -1)

def quarter_1st_day(thedate):
    quarternum_0based = int((thedate.month-1)/3)
    retmonth = quarternum_0based*3+1
    return castdate(("%d-%02d-%02d" % (thedate.year, retmonth, 1, )))
def quarter_last_day(thedate):
    return addmonths(quarter_1st_day(thedate), 3) + relativedelta(days = -1)

def halfyear_1st_day(thedate):
    halfyearnum_0based = int((thedate.month-1)/6)
    retmonth = halfyearnum_0based*6+1
    return castdate(("%d-%02d-%02d" % (thedate.year, retmonth, 1, )))
def halfyear_last_day(thedate):
    return addmonths(halfyear_1st_day(thedate), 6) + relativedelta(days = -1)

def year_1st_day(thedate):
    if type(thedate)==str:
        thedate = castdate(thedate)
    return castdate(("%d-%02d-%02d" % (thedate.year, 1, 1, )))
def year_last_day(thedate):
    #pdb.set_trace()
    if type(thedate)==str:
        thedate = castdate(thedate)
    return addyears(year_1st_day(thedate), 1) + relativedelta(days = -1)

def start_of_day(dt):
    #pdb.set_trace()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
def end_of_day(dt):
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
def roundtoday(dt):
    dt=castdatetime(dt)
    return "%d-%02d-%02d"%((dt).year, (dt).month, (dt).day, )

# Typecasts:
def castdatetime(strdate):
    return fields.Datetime.from_string(strdate)
def castdate(strdate):
    return fields.Date.from_string(strdate)
def date2str(thedate):
    return str(thedate)
def datetime2str(thedatetime):
    return str(thedatetime)

# Adders:
def adddays(thedate, ndays):
    return thedate + relativedelta(days=ndays)
def addmonths(thedate, nmonths):
    return thedate + relativedelta(months=nmonths)
def addyears(thedate, nyears):
    return thedate + relativedelta(years=nyears)

def is_whole_month_interval(start_date, end_date):
    if (    (start_date.day==1) and
            (start_date.month==end_date.month) and
            (end_date.month!=(end_date+timedelta(1)).month)):
        return True
    else:
        return False
def is_whole_year_interval(start_date, end_date):
    if not start_date or not end_date:
        return False
    end_date_plus_1day = adddays(end_date, 1)
    if (    (start_date.day==1) and (start_date.month==1) and
            (end_date_plus_1day.day==1) and (end_date_plus_1day.month==1) and
            (start_date.year==end_date.year)):
        return True
    else:
        return False

def covered_months(date_from, date_to):
    return (
        (date_to.year-date_from.year)*12
        + (date_to.month-date_from.month+1)
        )

# Helper classes to work with gregorian calendars:
class GregorianMonth:
    def __init__(self, year, month):
        """
        month is 1-based
        """
        assert ( 1 <= month <= 12 )
        self.year = year
        self.month = month
    def addMonths(self, nmonths):
        zb_month = (self.month-1)
        zb_newmonth = (zb_month+nmonths)%12
        newyear = self.year + (zb_month+nmonths)//12
        newmonth = zb_newmonth+1
        return GregorianMonth(newyear, newmonth)
    def subMonths(self, nmonths):
        return self.addMonths(-nmonths)
    def nextMonth(self):
        return self.addMonths(+1)
    def previousMonth(self):
        return self.addMonths(-1)
