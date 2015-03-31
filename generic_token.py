class Token(object):
    """A Token object must be an object with at least 3 attributes:
    - string representation of the token
    - a number that is the comparison to a 'positive' database set
    - a number that is the comparison to a 'negative' database set
    Token is initialized with a string that represents the value to be
    tested in the database."""
    def __init__(self, string):
        self.token_string = string
        self.positive_value = None
        self.negative_value = None
