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
                 global_description='',
                 positive_description='',
                 negative_description=''):
        """Creates the database schema if the file does not exist"""
        if not exists(database_path):
            self.db_connection = sl3.connect(database_path)        
            cursor = self.db_connection.cursor()
            cursor.execute("create table counters (counter INTEGER, name TEXT, description TEXT)")
            cursor.execute("insert into counters VALUES (0, 'global_counter', ?)", (global_description,))
            cursor.execute("insert into counters VALUES (0, 'positive_counter', ?)", (positive_description,))
            cursor.execute("insert into counters VALUES (0, 'negative_counter', ?)", (negative_description,))
            cursor.execute("create table negative_classification (token TEXT UNIQUE, count INTEGER)")
            cursor.execute("create table positive_classification (token TEXT UNIQUE, count INTEGER)")
            self.db_connection.commit()
            cursor.close()
        self.db_connection = sl3.connect(database_path)
    
    def update_counter(self, counter='', value=0):
        """Increment each counter according to train methods."""
        possible_counters = ['global_counter', 'positive_counter', 'negative_counter']
        if (not counter) or (counter not in positive_counters):
            return False
        cursor = self.db_connection.cursor()
        current = cursor.execute("SELECT counter from counters WHERE name=?", (counter))
        if current <= 0:
            return False
        current += value
        cursor.execute("UPDATE counters SET counter=? WHERE name=?", (current, counter))
        return True

    # TODO: execute many
    def _increment_or_insert(self, token, polarity=None):
        """for each token, if token not in database, add token to the database and set count to 1; if the
        token exists in the database, increment the counter by 1."""
        if not polarity:
            return False
        cursor = self.db_connection.cursor()
        try:
            if polarity == 'positive':
                cursor.execute("insert into positive_classification VALUES (?, ?)", (token, 1))
            elif polarity == 'negative':
                cursor.execute("insert into negative_classification VALUES (?, ?)", (token, 1))
        except sl3.IntegrityError: # token exists in database, so increment token count
            if polarity == 'positive':
                current = cursor.execute("SELECT count from positive_classification WHERE token=?", (token,))
                current += 1
                cursor.execute("UPDATE positive_classification SET count=? WHERE token=?", (current, token))
            elif polarity == 'negative':
                current = cursor.execute("SELECT count from negative_classification WHERE token=?", (token,))
                current += 1
                cursor.execute("UPDATE negative_classification SET count=? WHERE token=?", (current, token))
        finally:
            self.db_connection.commit()
            cursor.close()
        return None

    def _decrement_or_remove(self, token, polarity):
        """for each token, if token not in database, pass, else if token count >
        1, decrement, else if token count == 1, remove element from database"""
        if not polarity:
            return False
        cursor = self.db_connection.cursor()

        try:
            if polarity == 'positive':
                current_cursor = cursor.execute("SELECT count from positive_classification WHERE token=?", (token,))
                # current_cursor 
                current_value = current_cursor.fetchone()
                
                if not current_value: # not in database
                    return True
                else:
                    value = current_value[0]
                if value == 1: # remove the token from the database
                    
                    
                current -= 1
                cursor.execute("UPDATE positive_classification SET count=? WHERE token=?", (current, token))
            elif polarity == 'negative':
                current = cursor.execute("SELECT count from negative_classification WHERE token=?", (token,))
                current += 1
                cursor.execute("UPDATE negative_classification SET count=? WHERE token=?", (current, token))
        finally:
            self.db_connection.commit()
            cursor.close()
        return None

    # TODO: execute many
    def train_positive(self, tokens):
        """batch update/insert tokens and increment global and positive counters"""
        for token in tokens:
            self._increment_or_insert(token, polarity='positive')
        self.increment_counter('global_counter')
        self.increment_counter('positive_counter')
        return None

    def train_negative(self, tokens):
        """For each token in tokens, add token/counter and/or increment negative_counter in database.
        Increment the global counter"""
        for token in tokens:
            self._increment_or_insert(token, polarity='negative')
        self.increment_counter('global_counter')
        self.increment_counter('negative_counter')
        return None
    
    def untrain_positive(self, tokens):
        """for each token, if token in database increment the token's counter by 1.
        if token does not exist in the database, pass. If decrement_global_counter
        is True, decrement the global counter"""
    
    def untrain_negative(self, decrement_global_counter=True):
        """for each token, if token in database increment the token's counter by 1.
        if token does not exist in the database, pass. If decrement_global_counter
        is True, decrement the global counter"""
        pass
    
    
