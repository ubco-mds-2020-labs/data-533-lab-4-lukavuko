#!/usr/bin/env python
# coding: utf-8


from Mortgage_Package.mortgages.mortgages import *

import unittest

class Test_mortgages_Residential(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('!!! Class setup for Test(mortgages_Residential) !!!')
    
    def setUp(self):
        self.home1 = Residential(prop = 'The Bronson Home',        ## tested
                       price = 680000,                             ## tested
                       prop_owner = 'Brookfield Asset Management', ## tested
                       area = 'Quinterra', 
                       city = 'Ottawa',
                       prov = 'ON',                                ## tested
                       sq_footage = 2600,
                       year_built = 2003)
        self.home2 = Residential(prop = 'Mill Cottage',            ## tested
                       price = 1950260,                            ## tested
                       prop_owner = 'Big Houses Inc.',             ## tested
                       area = 'Rockcliff',
                       city = 'Ottawa',
                       prov = 'ON',                                ## tested
                       sq_footage = 8600,
                       year_built = 1926)
        print('~~~ start test ~~~')

    
    def test_getArea(self):
        self.assertEqual(self.home1.getArea(), 'Quinterra')
        self.assertEqual(self.home2.getArea(), 'Rockcliff')
        
        ## Change values
        self.home1.area = 'X'
        self.home2.area = 'Y'
        
        self.assertNotEqual(self.home1.getArea(), 'Quinterra')
        self.assertNotEqual(self.home2.getArea(), 'Rockcliff')
    
    
    def test_getCity(self):
        self.assertEqual(self.home1.getCity(), 'Ottawa')
        self.assertEqual(self.home2.getCity(), 'Ottawa')

        ## Change values
        self.home1.city = 'X'
        self.home2.city = 'Y'
        
        self.assertNotEqual(self.home1.getCity(), 'Quinterra')
        self.assertNotEqual(self.home2.getCity(), 'Rockcliff')
        
        
    def test_getSq_footage(self):
        self.assertEqual(self.home1.getSq_footage(), 2600)
        self.assertEqual(self.home2.getSq_footage(), 8600)
        
        ## Change values
        self.home1.sq_footage = 0
        self.home2.sq_footage = 0
        
        self.assertNotEqual(self.home1.getSq_footage(), 2600)
        self.assertNotEqual(self.home2.getSq_footage(), 8600)
        
        
    def test_getYear_built(self):
        self.assertEqual(self.home1.getYear_built(), 2003)
        self.assertEqual(self.home2.getYear_built(), 1926)
    
        ## Change values
        self.home1.year_built = 0
        self.home2.year_built = 0
        
        self.assertNotEqual(self.home1.getYear_built(), 2600)
        self.assertNotEqual(self.home2.getYear_built(), 8600)   
    
    
    def test__repr__(self):
        self.assertEqual(repr(self.home1), f'''{self.home1.prop}\n    Price: ${self.home1.price}\n    Legal owner : {self.home1.prop_owner}\n    Area: {self.home1.area}\n    City: {self.home1.city}\n    Province: {self.home1.prov}\n    Square Footage: {self.home1.sq_footage}\n    Year Built: {self.home1.year_built}''')
        
        self.assertEqual(repr(self.home2), f'''{self.home2.prop}\n    Price: ${self.home2.price}\n    Legal owner : {self.home2.prop_owner}\n    Area: {self.home2.area}\n    City: {self.home2.city}\n    Province: {self.home2.prov}\n    Square Footage: {self.home2.sq_footage}\n    Year Built: {self.home2.year_built}''')
        
        
    def test__str__(self):
        self.assertEqual(str(self.home1), f'''{self.home1.prop}\n    Price: ${self.home1.price}\n    Legal owner : {self.home1.prop_owner}\n    Area: {self.home1.area}\n    City: {self.home1.city}\n    Province: {self.home1.prov}\n    Square Footage: {self.home1.sq_footage}\n    Year Built: {self.home1.year_built}''')
        
        self.assertEqual(str(self.home2), f'''{self.home2.prop}\n    Price: ${self.home2.price}\n    Legal owner : {self.home2.prop_owner}\n    Area: {self.home2.area}\n    City: {self.home2.city}\n    Province: {self.home2.prov}\n    Square Footage: {self.home2.sq_footage}\n    Year Built: {self.home2.year_built}''')

        
    def tearDown(self):
        print('~~~ complete ~~~')  
        
    @classmethod
    def tearDownClass(cls):
        print('!!! Class teardown for Test(mortgages_Residential) !!!\n\n\n')


#unittest.main(argv=[''], verbosity=2, exit=False)





