from naive_bayes_db import NaiveBayesDB
        
class NaiveBayesClassifier(object):
    """High level naive Bayes classifier.
    If the database exists, instantiate class, within NaiveBayesDB;
    if the database does not exist, create one and use the descriptions
    given in __init__(), or '' for each if none are given"""
    def __init__(self, database_path,
                 global_description='',
                 positive_description='',
                 negative_description=''):
        """Accepts 2 databases for which a token would be 
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
    def _get_ratios(self):
        total_positive = self.database.total_for_polarity(polarity='positive')
        total_negative = self.database.total_for_polarity(polarity='negative')
        for token in self.tokens:
            positive_count = self.database.counter_for_token(token.token_string,
                                                    polarity='positive')
            negative_count = self.database.counter_for_token(token.token_string,
                                                    polarity='negative')
            numerator = (positive_count/total_positive)
            denominator = ((positive_count/total_positive) + (negative_count/total_negative))
            print("%f / %f" % (numerator, denominator))
            token.positive_value = numerator/denominator
            numerator = (negative_count/total_negative)
            denominator = ((negative_count/total_negative) + (positive_count/total_positive))
            token.negative_value = numerator/denominator
        return True
            
    def sum_positive(self):
        """p(S) = (p1 * p2 ... pn) / 
        ( (p1 * p2 ... * pn) + ( (1 - p1) * (1 - p2) ... * (1 - pn) ) )"""
        numerator = sum([token.positive_value for token in self.tokens])
        denominator = numerator + sum([1-token.positive_value for token in self.tokens])
        print("%f / %f" % (numerator, denominator))
        return numerator/denominator
            
    def sum_negative(self):
        """p(S) = (p1 * p2 ... pn) / 
        ( (p1 * p2 ... * pn) + ( (1 - p1) * (1 - p2) ... * (1 - pn) ) )"""
        numerator = sum([token.negative_value for token in self.tokens])
        denominator = numerator + sum([1-token.negative_value for token in self.tokens])
        print("%f / %f" % (numerator, denominator))
        return numerator/denominator

        
            
        
