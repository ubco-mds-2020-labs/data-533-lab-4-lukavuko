#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest


# In[2]:


from Test_Scripts.Test_mortgages_RealEstate import *
from Test_Scripts.Test_mortgages_Residential import *
from Test_Scripts.Test_mortgageEstimator_base import *
from Test_Scripts.Test_mortgageEstimator_propFilter import *

from Test_Scripts.Test_debtServiceRatio_ratio import *
from Test_Scripts.Test_debtServiceRatio_mortgage import *
from Test_Scripts.Test_cr_conversion import *
from Test_Scripts.Test_cr_score import *


# In[3]:


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    
    suite.addTest(unittest.makeSuite(Test_mortgages_RealEstate))
    suite.addTest(unittest.makeSuite(Test_mortgages_Residential))
    suite.addTest(unittest.makeSuite(Test_mortgage_estimator_base_functions))
    suite.addTest(unittest.makeSuite(Test_mortgage_estimator_propertyfilter))
    
    suite.addTest(unittest.makeSuite(Test_debtServiceRatio_ratio))
    suite.addTest(unittest.makeSuite(Test_debtServiceRatio_mortgage))
    suite.addTest(unittest.makeSuite(Test_cr_conversion))
    suite.addTest(unittest.makeSuite(Test_cr_score))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()


# In[ ]:




