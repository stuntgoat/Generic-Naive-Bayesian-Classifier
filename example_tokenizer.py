import generic_token as tkn 
import re

class SpamTokenizer(object):
    """parse email content, given as a list of strings- a list of lines in a file."""
    def __init__(self, items):
        """Accepts: a list of email 'body' lines.
        Returns: a list of tokens"""
        self.items = items
        self.tokens = []

    def parse_pre_tokens(self, symbol):
        """remove '=', '><', and any word that does not contain letters; or
        if the word 'spam' occurs, remove that word from the token list. 
        remove cruft from html."""
        if ('=' in symbol) or ('><' in symbol):
            return None
        spam_in_subject = re.compile('spam', re.I)
        if re.search(spam_in_subject, symbol):
            return None
        token = symbol.rstrip("'\"(<>*%$#@!:?,.\/").lstrip("'\")\/<>*%$#@!?:,.")
        if re.search("[a-zA-Z]{3,}", token) and (len(token) < 13):
            return token
        return None

    def tokenize(self):
        """Override this method to process the data_container
        Returns: this must return a list of Token objects."""
        split_tokens = []
        for item in self.items:
            split_string = item.split()
            split_tokens.extend(split_string)
        for pre_token in split_tokens:
            t = self.parse_pre_tokens(pre_token)
            if t and (t not in self.tokens):
                self.tokens.append(tkn.Token(t))
        return self.tokens

                

 
