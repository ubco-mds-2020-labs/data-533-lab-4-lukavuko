# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
class financialError(Exception):
    '''Financial subpackage custom exception class.'''
    pass

class residenceError(financialError):
    '''Raised when residence status is not 'own' or 'rent'.'''
    pass

class incomeError(financialError):
    '''Raised when income input is below 10000.'''
    pass


