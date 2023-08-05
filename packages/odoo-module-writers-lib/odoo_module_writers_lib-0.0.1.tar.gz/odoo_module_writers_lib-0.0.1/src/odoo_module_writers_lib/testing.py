# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: João Jerónimo (joao.jeronimo.pro@gmail.com)
#    Copyright (C) 2019-2022 - Licensed under the terms of GNU LGPL
#
##############################################################################

class AssertLib:
    # For numbers:
    def assertZero(self, num):
        self.assertEqual( 0, num )
    
    # For collections:
    def assertLength(self, collection, thelen):
        self.assertEqual( len(collection), thelen )
    def assertEmpty(self, collection):
        self.assertLength( collection, 0 )
    def assertNotEmpty(self, collection):
        self.assertGreater( len(collection), 0 )
    def assertSingleton(self, collection):
        self.assertLength( collection, 1 )
    def assertCorrectOrder(self, collection, can_one_appear_before_other, elem_to_str):
        """
        Assert that a coolection is in the correct oreder.
        can_one_appear_before_other     Predicate that returnas true if its first arg is
                                        supposed to appear before its the second arg.
        """
        for i in range(len(collection)-1):
            one   = collection[i]
            other = collection[i+1]
            self.assertTrue(
                can_one_appear_before_other(one, other),
                "Collection %s (or %s) is out of other: %s should appear before %s." % (
                    str(collection),
                    str([elem_to_str(colleem) for colleem in collection]),
                    elem_to_str(one),
                    elem_to_str(other),
                    )
                )
    
    # For strings:
    def assertStringContains(self, the_string, to_search):
        self.assertNotEqual( the_string, False )
        self.assertEqual( type(the_string), str )
        self.assertNotEqual( len(the_string), 0 )
        lowered = the_string.lower()
        self.assertTrue(
                any([ tf in lowered for tf in to_search ]),
                msg="String %s contains none of the strings: %s" % (lowered, repr(to_search), ) )
    def assertStringNotContains(self, the_string, to_search):
        lowered = the_string.lower()
        for ft in to_search:
            self.assertFalse( tf in lowered )

class JournalEnsures:
    def aux_ensure_cash(self, journal):
        self.assertEqual( 'cash', journal.type )
    
    def aux_ensure_bank(self, journal):
        self.assertEqual( 'bank', journal.type )

class PaymentEnsures:
    def aux_ensure_outbound_cash(self, payment):
        self.assertEqual( 'outbound', payment.payment_type )
        self.aux_ensure_cash( payment.journal_id )
    
    def aux_ensure_deposit(self, payment):
        self.assertEqual( 'transfer', payment.payment_type )
        self.aux_ensure_cash( payment.journal_id )
        self.aux_ensure_bank( payment.destination_journal_id )
    
    def aux_ensure_withdrawal(self, payment):
        self.assertEqual( 'transfer', payment.payment_type )
        self.aux_ensure_bank( payment.journal_id )
        self.aux_ensure_cash( payment.destination_journal_id )

class BankStatementEnsures:
    def aux_ensure_stmtline_is_reconciled(self, stmtline):
        self.assertNotEmpty( stmtline.journal_entry_ids )
