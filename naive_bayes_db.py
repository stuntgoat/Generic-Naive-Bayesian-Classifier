import sqlite3 as sl3
from os.path import exists

class NaiveBayesDB(object):
    """Creates and maintains a database that will 
    hold values for the NaiveBayesClassifier.
    TODO: 
    - try/execpt database creation or read/write error; test using os.stat
    - if file exists, test for permissions to read/write, also check size
    """
    def __init__(self, database_path, 
                 global_description=None,
                 positive_description=None,
                 negative_description=None):
        """Creates the database schema if it the file does not exist"""
        if not exists(database_path):
            self.db_connection = sl3.connect(database_path)        
            curser = self.db_connection.curser()
            curser.execute("create table counters (counter INTEGER, name TEXT, description TEXT)")
            curser.execute("insert into counters (0, 'global_counter', ?)", global_description)
            curser.execute("insert into counters (0, 'positive_counter', ?)", positive_description)
            curser.execute("insert into counters (0, 'negative_counter', ?)", negative_description)
            curser.execute("create table negative_classification (tokens TEXT, count INTEGER)")
            curser.execute("create table positive_classification (tokens TEXT, count INTEGER)")
            self.db_connection.commit()
            curser.close()
        self.db_connection = sl3.connect(database_path)
    
    def train_positive(self):
        """for each token, if token not in database, add token to the database and set count to 1; if the
        token exists in the database, increment the counter by 1."""
        pass

    def untrain_positive(self, decrement_global_counter=True):
        """for each token, if token in database increment the token's counter by 1.
        if token does not exist in the database, pass. If decrement_global_counter
        is True, decrement the global counter"""
        pass

    def train_negative(self):
        """For each token in tokens, add token/counter and/or increment negative_counter in database.
        Increment the global counter"""
        pass
    
    def untrain_negative(self, decrement_global_counter=True):
        """for each token, if token in database increment the token's counter by 1.
        if token does not exist in the database, pass. If decrement_global_counter
        is True, decrement the global counter"""
        pass
    
    
