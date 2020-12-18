#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings, pandas as pd, numpy as np
from Mortgage_Package.mortgages.exceptions import *

# In[4]:


def property_filter(property_data, downpayment, mortgage_rate = None, mortgage_term = None, max_monthly_payment = None, max_loan = None):
    ''' Returns a dataframe containing the properties/areas.
        
    Arguments
    ----------
    data : dataframe 
        Areas/properties in column index 0 (str)
        Respective prices in column index 1 (numeric) 
        
    downpayment : numeric
        Your maximal downpayment
    
    mortgage_rate : numeric 
        Interest rate on the mortgage loan (leave empty if mortgage_term is provided)
    
    mortgage_term : int 
        Contract length in years (1 to 10) for the mortgage interest rate.
        Only specify if you do not know what mortgage_rate to enter (leave empty if mortgage_rate provided)
        
    max_monthly_payment : numeric 
        Your max affordable or bank limited monthly payment towards your home
        
    max_loan : numeric
        Max eligible loan based on your downpayment

    Return
    ------
    dataframe
        Properties/Areas
        Prices/Average area price
        Minimum_Downpayment
        Mortgage_Insurance
        Principal
        Monthly_Payment
        Shortest_Amortization
        Total_Interest
        Net_Cost (assuming no other fees)
        '''
    
    warnings.filterwarnings("ignore") 
    
    try:
        # is object a dataframe?
        if isinstance(property_data, pd.DataFrame) == False:
            raise FilterInputError('Dataframe object expected')
        # right number of columns?
        if len(property_data.columns)!=2:
            raise FormatError('Expected two columns of type str and numeric, respectively')
        # is column at index 1 (price) numeric?
        if pd.api.types.is_numeric_dtype(property_data.iloc[:,1]) == False:
            raise TypeError('Column at index 1 (price) must be numeric')
            
    except FilterInputError as FIE:
        print(FIE, '\nReveived object of type:', type(property_data))
        return None
    except FormatError as FE:
        print(FE,'\nReveived dataframe with this many columns:', len(property_data.columns))
        return None       
    except TypeError as TE:
        print(TE)
        return None
    
    data = property_data.copy()
    
    # Rename columns
    data.set_axis(['Property/Area', 'Price'], axis=1, inplace=True)
    
    # Note original input of properties
    og_prop_count = data['Property/Area'].count()
    
    # FILTER: Downpayment. Remove properties where minimal DP exceeds your entered DP
    data['Minimum_Downpayment'] = data.iloc[:, 1].apply(lambda x: min_downpayment(x))
    data = data[data['Minimum_Downpayment'] <= downpayment]
    
    # Mortgage rate. If none provided give a reasonable estimate
    if mortgage_rate == None:
        mortgage_rate = mort_rate(mortgage_term)
    
    # Calculate mortgage insurance lump sum for each property
    default_insurance = []
    for price in data['Price']:
        default_insurance +=  [mortgage_insurance(price, downpayment)]
    data['Mortgage_Insurance'] = default_insurance
    
    # Calculate initial principal for each property by converting annual mortgage rate to a monthly rate
    data['Principal'] = round((data['Price'] - downpayment + data['Mortgage_Insurance']), 2)
    
    # FILTER: Max eligible loan. Remove properties where the principal exceeds you max approved loan.
    data = data[data['Principal'] < max_loan]
    
    # Add two columns for monthly payment and shortest amortization period
    Monthly_Payment = []; Amortization = []
    for princ in data['Principal']:
        Monthly_Payment += [optimal_monthly_payment(princ, mortgage_rate, max_monthly_payment)[0]]
        Amortization += [optimal_monthly_payment(princ, mortgage_rate, max_monthly_payment)[1]]
    data['Monthly_Payment'] = Monthly_Payment
    data['Shortest_Amortization'] = Amortization
    
    # FILTER: Remove rows where Monthly_Payment is null
    data = data[data['Monthly_Payment'].notnull()]
    
    # Add column for the cumulative cost of interest given that amortization
    tot_int = []
    for princ, monthly_payment in data[['Principal', 'Monthly_Payment']].itertuples(index=False):
        tot_int += [total_interest(princ, mortgage_rate, monthly_payment)]
    data['Total_Interest'] = tot_int
    
    # Add column for net cost of home (price + cumulative interest + mortgage insurance)
    data['Net_Cost'] = data['Price'] + data['Mortgage_Insurance'] + data['Total_Interest']
    
    print(f"You can afford {data['Property/Area'].count()} properties from the {og_prop_count} you've provided.")
    return data


# In[1]:


def min_downpayment(price):
    ''' Returns the minimum downpayment required for a real estate
    price defined by the Financial Consumer Agency of Canada.
    (https://www.canada.ca/en/financial-consumer-agency/services/mortgages/down-payment.html)
    
    Arguments
    ----------
    price : numeric
        Property price or avereage area property price
    
    Return
    ------
    float
        minimum downpayment
    '''
    try:
        if  price < 0:
            print("Invalid price")
            return None
        elif price < 500000:
            return price*0.05
        elif price < 1000000:
            return (500000*0.05 + (price - 500000)*0.1)
        return price*0.2
    
    except TypeError:
        print("Invalid price input. Must be of type numeric")
        return None


# In[33]:


def mort_rate(term):
    ''' If no mortgage rate is specified this function can be used to
    return an estimated mortgage rate based on a regression fit (R^2 = 0.926)
    on average Canadian mortgage rates for possible term lengths.
    (https://www.superbrokers.ca/tools/mortgage-rates-comparison/)
        
    Arguments
    ----------
    term : int
        contract length in years (from 1 to 10 years)
        
    Return
    ------
    float
        interest rate
    '''
    try:
        if term < 1:
            raise TermError
        elif term > 10:
            raise TermError('Lengths greater than 10 years are not typically available.')
        elif isinstance(term, float):
            print('Warning: Term lengths are typically in whole years not fractions of years.')
        
        x = term
        return round((0.0167*x**2 - 0.0337*x + 1.6851), 3)
    
    except TermError as TE:
        print(f'{TE} Terms must range from (1,10) years.')
        return None
        


# In[6]:


def mortgage_insurance(price, downpayment):
    ''' Returns the cost of mortgage insurance.
    
    Insurance rates are calculated from loan to asset price ratio.
    Rates are applied to the loan to generate a lump sum amount that's
    then added to the principal of the loan to give mortgage insurance.
    
    Arguments
    ----------
    price : numeric
        Property price
    
    downpayment : int or float
        Downpayment on property
        
    Return
    ------
    float
        Mortgage insurance
    '''
    try:
        DP_proportion = downpayment / price

        # if downpayment more than 20% of the house price no mortgage insurance required.
        if DP_proportion >= 0.2:
            return 0
        elif DP_proportion < 0.05:
            raise PovertyError('Downpayment must be at least 5% the asset value')

        loan_to_price = (price-downpayment)/price
        x = loan_to_price

        # loan to price ratio determines insurance rate
        insurance_rate = (2924.5*x**4 - 9340.3*x**3 + 11116*x**2 - 5830.8*x + 1137.1)/100

        # mortgage insurance is a % applied to the mortgage amount (price - downpayment)
        return round(((price - downpayment) * insurance_rate), 2)
    
    except TypeError:
        print('Bad entry type. Received:', type(price), type(downpayment))
        return None
    except PovertyError as PE:
        print(PE, '\nInput value is too low to be legally considered.')
        return None
    except ZeroDivisionError:
        print('Price cannot be zero.')
        return None    


# In[12]:


def optimal_monthly_payment(principal, mortgage_rate, max_monthly_payment):
    ''' Returns the first amortization period which has a monthly payment
    less than your max_monthly_payment (ie. within budget). The shortest
    possible amortization period has the lowest long term interest cost.

    Arguments
    ----------
    principal : numeric
    
    mortgage_rate : float
          Annual mortgage rate (loan interest)
    
    max_monthly_payment: numeric
        Your max affordable monthly contribution
    
    Return
    ------
    list
        mp: monthly payment for a given amortization
        i: amortization period in years
    '''
    try:
        for i in range(1, 26):
            mp = monthly_payment(principal, mortgage_rate, i, months = False)
            if mp <= max_monthly_payment:
                return [mp, i]
        return [np.nan, np.nan]
    
    except TypeError:
        print('Bad entry type. Received:', type(principal), type(mortgage_rate), type(max_monthly_payment))
        return None


# In[14]:


def monthly_payment(principal, mortgage_rate, amortization, months = False):
    ''' Returns the monthly payment required to meet the given amortization period.
    Assumes payments occur on a monthly basis.

    Arguments
    ----------
    principal : numeric
    
    mortgage_rate : float
        Annual mortgage rate (loan interest)
    
    amortization: int
        Amortization period in years (or in months if months == True)
        
    months : bool 
        (Optional) if True, amortization period is interpreted in months (default = False)
    
    Return
    ------
    float
        monthly payment
    '''
    
    R = (mortgage_rate/100/12 + 1)   ## monthly interest rate
    
    if months == True:
        n = amortization ## if specified in months, amortization = the number of payments 
    n = amortization*12 ## convert amortization in years to the number of monthly payments
        
    monthly_contribution = principal*((R**n)*(1-R) / (1-R**n))
    
    return round(monthly_contribution, 2)


# In[19]:


def total_interest(principal, mortgage_rate, monthly_payment):
    ''' Returns the cumulative interest paid on a given principal, mortgage rate, and monthly payment.
    
    Arguments
    ----------
    principal : numeric
    
    mortgage_rate : float
        Annual mortgage rate (loan interest)
    
    amortization: int
        Amortization period in years (or in months if months == True)
        
    monthly_payment : bool 
        Monthly contribution towards the principal
    
    Return
    ------
    float
        Cumulative interest paid
    '''
    try:
        R = mortgage_rate/1200   ## monthly interest rate
        CumInterest = 0

        i = principal * R
        new_p = principal + i - monthly_payment

        while new_p > 0:
            CumInterest += i
            i = new_p * R
            new_p = new_p + i - monthly_payment

            if new_p >= new_p - i + monthly_payment:
                print("Monthly contribution is insufficient to pay off the original Principal.")
                return None

        return round(CumInterest, 2)
    
    except TypeError:
        print('Bad entry type. Received:', type(principal), type(mortgage_rate), type(monthly_payment))
        return None

