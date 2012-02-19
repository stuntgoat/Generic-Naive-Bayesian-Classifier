
        
class NaiveBayesClassifier(object):
    """High level naive Bayes classifier. """
    def __init__(self, positive_db=positive_db, negative_db=negative_db):
        """Accepts 2 databases for which a token would be 
        tested positive and negative."""
        self.positive_db = positive_db
        self.negative_db = negative_db
        self.tokens = None
    
    def test_token(self, tokens):
        """Accepts: a list of tokens to compare to each database.
        Returns: a list of updated tokens that have the values
        updated for the respective databases"""
        # run query of each token in the database
        
        # setting the value of the respective Token value
    ##############################
    # database operations call NaiveBayesDB functions to abstract db interactions
    # from this class
    def train_positive(self):
        """For each token in self.tokens, add token/counter to positive_classification,
        and/or increment positive_counter in database"""
        pass

    def untrain_positive(self):
        """For each token in tokens, decrement token counter in positive_classification.
        If token counter == 0, remove token from table"""
        if not self.tokens:
            return self.tokens
        pass

    def train_negative(self):
        """For each token in tokens, add token/counter to negative_classification, 
        and/or increment negative_counter in database."""
        if not self.tokens:
            return self.tokens
        pass

    def untrain_negative(self):
        """For each token in tokens, decrement token counter in negative_classification.
        If token counter == 0, remove token from table"""
        pass
    ##############################
    # bayes formula operations
        
            
        
