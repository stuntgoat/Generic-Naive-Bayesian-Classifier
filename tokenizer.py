
class Tokenizer(object):
    """ """
    def __init__(self, data_container):
    """Accepts: a function and a raw container of data to process with the function"""
        self.data_container = data_container
        self.token_list = []
    
    
    def process_container(self):
        """Override this method to process the data_container
        Returns: this must return a list of Token objects."""
        return self.token_list
