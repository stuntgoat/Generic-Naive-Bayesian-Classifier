


        
class NaieveBayesClassifier(object):
    """Currently supports sqlite for comparing tokens"""
    def __init__(self, positive_db, negative_db):
        """Accepts 2 databases for which a token would be 
        tested positive and negative."""

        self.positive_db = positive_db
        self.negative_db = negative_db
        self.tokens = None

    def compare_tokens(self, tokens):
        """Accepts: a list of tokens to compare to each database.
        Returns: a list of updated tokens that have the values
        updated for the respective databases"""
        # run query of each token in the database
        pass

    def train(database):
        pass

        
        
        
