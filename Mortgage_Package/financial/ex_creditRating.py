# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
class residenceError(Exception):
    def __init__(self):
        print("Determine if current residence status is 'own' or 'rent'.")

class incomeError(Exception):
    def __init__(self):
        print("Income is too low to be considered for a credit rating.")

#class 1 - converts client's information into score
class creditRating:
    """
    A class used to convert home buyer's financial characteristics into individual credit score components
    
    ...

    Attributes
    ----------
    age : int
        home buyer's age in years
    home : str
        home buyer's current residence status; own or rent
    income : int
        home buyer's annual income
    score_age : int
        points awarded to credit score based on home buyer's age
    score_home : int
        points awarded to credit score based on home buyer's current residence status
    score_income : int
        points awarded to credit score based on home buyer's annual income

    Methods
    -------
    convert_age()
        converts home buyer's age into points based on 7 possible age ranges
    convert_home()
        converts home buyer's current residence status into points based on 2 possible residence statuses
    convert_income()
        converts home buyer's annual income into points based on 6 possible annual income ranges

    """
    
    score_age = 0
    score_home = 0
    score_income = 0

    def __init__(self, age, home, income):
        """
        Arguments
        ---------
        age : int
        home : int
        income : int
        """
        
        self.age = age
        self.home = home
        self.income = income
        

    def convert_age(self): #works
        """
        Returns age score, converting home buyer's age into points after comparing 7 possible age ranges
        """
        
        try:
            if self.age < 22:
                score_age = 100
            elif self.age < 26:
                score_age = 120
            elif self.age < 29:
                score_age = 185
            elif self.age < 32:
                score_age = 200
            elif self.age < 37:
                score_age = 210
            elif self.age < 42:
                score_age = 225
            else:
                score_age = 250
        
            return score_age
        
        except TypeError:
            print("Invalid age input. Age input must be of type numeric.")
            return None
    
    def convert_home(self): #works
        """
        Returns home score, converting home buyer's current residence status into points depending on if they own 
    or rent
        """

        try:
            if self.home.lower() == "own":
                score_home = 225
            elif self.home.lower() == "rent":
                score_home = 100
            else:
                raise residenceError
                #print("Please choose between 'own' or 'rent'.")
        
            return score_home
        
        except residenceError:
            print("Please input either 'own' or 'rent'.")
            return None

    def convert_income(self): #works
        """
        Returns income score, converting home buyer's annual income into points after comparing 6 possible income ranges
        """

        try:
            if self.income < 10000:
                raise incomeError
            elif self.income >= 10000 and self.income < 17000:
                score_income = 140
            elif self.income >= 17000 and self.income < 26000:
                score_income = 180
            elif self.income >= 26000 and self.income < 35000:
                score_income = 200
            elif self.income >= 35000 and self.income < 42000:
                score_income = 225
            elif self.income >= 42000 and self.income < 58000:
                score_income = 230
            elif self.income >= 58000:
                score_income = 260

            return score_income

        except incomeError:
            print("Inputted salary is too low to be considered for a credit rating")
            return None

        except TypeError:
            print("Invalid salary input. Salary input must be of type numeric.")
            return None


# %%
def score(buyer):
    """
    Prints calculated score with decision of loan approval.
    Calculates credit score with individual component scores from class creditRating to determine loan approval.
    ...
    
    Argument
    --------
    buyer : object
        object from class creditRating

    Return
    ---------
    score : int
        sum of component scores age + home + income
    """

    score = buyer.convert_age() + buyer.convert_home() + buyer.convert_income()

    try:
        if score >= 500:
            print("Credit Score: {}. Approved for loan.".format(score))
        else:
            print("Credit Score: {}. Not approved for loan.".format(score))

        return score

    except NameError:
        print("Invalid buyer name. Input correct buyer name.")
        return None


# %%
buyer_credit_rating = creditRating(20, "OWN", 60000)


# %%
buyer_credit_rating.convert_age()


# %%
buyer_credit_rating.convert_home()


# %%
buyer_credit_rating.convert_income()


# %%
score(buyer_credit_rating)


# %%



# %%



