from token import Token

class Tokenizer(object):
    """ """
    def __init__(self, items):
    """Accepts: a function and a raw container of data to process with the function"""
        self.items = items
        self.tokens = []
    
    def tokenize(self):
        """Override this method to process the data_container
        Returns: this must return a list of Token objects."""
        for item in items:
            self.tokens.append(Token(item))
        return self.tokens
    
