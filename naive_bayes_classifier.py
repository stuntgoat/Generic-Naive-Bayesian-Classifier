from naive_bayes_db import NaiveBayesDB
         
class NaiveBayesClassifier(object):
    """High level naive Bayes classifier.
    NaiveBayesDB will create the database if database_path
    does not exist. Use descriptions when creating a new database."""
    def __init__(self, database_path,
                 global_description='',
                 positive_description='',
                 negative_description=''):
        """Accepts a database where a token would be 
        tested positive and negative."""
        self.database = NaiveBayesDB(database_path,
                                     global_description=global_description,
                                     positive_description=positive_description,
                                     negative_description=negative_description)
        self.tokens = None

    def register_tokens(self, tokens):
        self.tokens = tokens
        return None
    
    ##############################
    # database operations call NaiveBayesDB functions to abstract db interactions
    # from this class
    def train_positive(self):
        """For each token in self.tokens, add token/counter to positive_classification,
        and/or increment positive_counter in database"""
        self.database.train_positive(self.tokens)
        return None

    def untrain_positive(self):
        """For each token in tokens, decrement token counter in positive_classification.
        If token counter == 0, remove token from table"""
        self.database.untrain_positive(self, tokens)
        return None

    def train_negative(self):
        """For each token in tokens, add token/counter to negative_classification, 
        and/or increment negative_counter in database."""
        self.database.train_negative(self.tokens)
        return None

    def untrain_negative(self):
        """For each token in tokens, decrement token counter in negative_classification.
        If token counter == 0, remove token from table"""
        self.database.untrain_negative(self, tokens)

    ##############################
    # bayes formula operations
    def calculate_probabilities(self):
        """Stores the Token.token_string values, as compared positive and negative
        in the database, within the Token.positive_value and Token.negative_value,
        respectively."""
        total_positive = self.database.total_for_polarity(polarity='positive')
        total_negative = self.database.total_for_polarity(polarity='negative')
        for token in self.tokens:
            positive_count = self.database.counter_for_token(token.token_string,
                                                             polarity='positive')
            negative_count = self.database.counter_for_token(token.token_string,
                                                             polarity='negative')
            numerator = (float(positive_count)/total_positive)
            denominator = ((float(positive_count)/total_positive) + (float(negative_count)/total_negative))
            token.positive_value = numerator/denominator
            numerator = (float(negative_count)/total_negative)
            denominator = ((float(negative_count)/total_negative) + (float(positive_count)/total_positive))
            token.negative_value = numerator/denominator
        return True
            
    def sum_positive(self):
        """p(S) = (p1 * p2 ... pn) / 
        ( (p1 * p2 ... * pn) + ( (1 - p1) * (1 - p2) ... * (1 - pn) ) )"""
        numerator = sum([token.positive_value for token in self.tokens])
        denominator = numerator + sum([1-token.positive_value for token in self.tokens])
        return float(numerator)/denominator
            
    def sum_negative(self):
        """p(S) = (p1 * p2 ... pn) / 
        ( (p1 * p2 ... * pn) + ( (1 - p1) * (1 - p2) ... * (1 - pn) ) )"""
        numerator = sum([token.negative_value for token in self.tokens])
        denominator = numerator + sum([1-token.negative_value for token in self.tokens])
        return float(numerator)/denominator

        
            
        
