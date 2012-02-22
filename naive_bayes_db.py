import sqlite3 as sl3
from os.path import exists

class NaiveBayesDB(object):
    """Creates and maintains a database that will 
    hold values for the NaiveBayesClassifier.
    TODO: 
    - try/execpt database creation or read/write error; test using os.stat
    - if file exists, test for permissions to read/write, also check size
    """
    def __init__(self,
                 database_path,
                 global_description='',
                 positive_description='',
                 negative_description=''):
        """Creates the database schema if the file does not exist"""
        if not exists(database_path):
            self.db_connection = sl3.connect(database_path)        
            self.db_connection.text_factory = str
            cursor = self.db_connection.cursor()
            
            cursor.execute("create table counters (counter INTEGER, name TEXT, description TEXT)")
            cursor.execute("insert into counters VALUES (0, 'global_counter', ?)", (global_description,))
            cursor.execute("insert into counters VALUES (0, 'positive_counter', ?)", (positive_description,))
            cursor.execute("insert into counters VALUES (0, 'negative_counter', ?)", (negative_description,))
            cursor.execute("create table negative_classification (token BLOB UNIQUE, count INTEGER)")
            cursor.execute("create table positive_classification (token BLOB UNIQUE, count INTEGER)")
            self.db_connection.commit()
            cursor.close()
        self.db_connection = sl3.connect(database_path)
        self.db_connection.text_factory = str
        self.cursor = None

    def update_counter(self, counter='', value=0):
        """Increment each counter according to train methods."""
        possible_counters = ['global_counter', 'positive_counter', 'negative_counter']
        if (not counter) or (counter not in possible_counters):
            return False
        current = self.cursor.execute("SELECT counter from counters WHERE name=?", (counter,))
        current_value = current.fetchone()[0]
        if (current_value == 0) and (value < 1):
            return False
        current_value += value
        self.cursor.execute("UPDATE counters SET counter=? WHERE name=?", (current_value, counter))
        return True
 
    # TODO: execute many
    def _increment_or_insert(self, token, polarity=None):
        """for each token, if token not in database, add token to the database and set count to 1; if the
        token exists in the database, increment the counter by 1."""
        if not polarity:
            return False

        try:
            if polarity == 'positive':
                self.cursor.execute("insert into positive_classification VALUES (?, ?)", (token, 1))
            elif polarity == 'negative':
                self.cursor.execute("insert into negative_classification VALUES (?, ?)", (token, 1))
        except sl3.IntegrityError: # token exists in database, so increment token count
            if polarity == 'positive':
                self.cursor.execute("SELECT count from positive_classification WHERE token=?", (token,))
                value = self.cursor.fetchone()[0]
                value += 1
                self.cursor.execute("UPDATE positive_classification SET count=? WHERE token=?", (value, token))
            elif polarity == 'negative':
                self.cursor.execute("SELECT count from negative_classification WHERE token=?", (token,))
                value = self.cursor.fetchone()[0]
                value += 1
                self.cursor.execute("UPDATE negative_classification SET count=? WHERE token=?", (value, token))
        finally:
            pass
        return None

    def _decrement_or_remove(self, token, polarity):
        """for each token, if token not in database, pass, else if token count >
        1, decrement, else if token count == 1, remove element from database"""
        if (not polarity) or (polarity not in ['positive', 'negative']):
            return False
        try:
            if polarity == 'positive':
                self.cursor.execute("SELECT count from positive_classification WHERE token=?", (token,))
                # current_cursor 
                current_value = self.cursor.fetchone()
                if not current_value: # not in database; do nothing
                    return True
                value = current_value[0]
                if value == 1: # remove the token from the database instead of setting to 0
                    self.cursor.execute("DELETE FROM positive_classification WHERE token=?", (token,))
                else: # decrement
                    value -= 1
                    self.cursor.execute("UPDATE positive_classification SET count=? WHERE token=?", (value, token))
            else:
                self.cursor.execute("SELECT count from negative_classification WHERE token=?", (token,))
                current_value = self.cursor.fetchone()
                if not current_value: # not in database; do nothing
                    return True
                value = current_value[0]
                if value == 1: # remove the token from the database instead of setting to 0
                    self.cursor.execute("DELETE FROM negative_classification WHERE token=?", (token,))
                else: # decrement
                    value -= 1
                self.cursor.execute("UPDATE negative_classification SET count=? WHERE token=?", (value, token))
        finally:
            pass
        return None

    # TODO: execute many
    def train_positive(self, tokens):
        """batch update/insert tokens and increment global and positive counters"""
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN TRANSACTION')
        for token in tokens:
            self._increment_or_insert(token.token_string, polarity='positive')
        self.update_counter('global_counter', value=1)
        self.update_counter('positive_counter', value=1)
        self.db_connection.commit()
        self.cursor.close()
        return None

    def train_negative(self, tokens):
        """For each token in tokens, add token/counter and/or increment negative_counter in database.
        Increment the global counter"""

        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN TRANSACTION')
        for token in tokens:
            self._increment_or_insert(token.token_string, polarity='negative')
        self.update_counter('global_counter', value=1)
        self.update_counter('negative_counter', value=1)
        self.db_connection.commit()
        self.cursor.close()
        return None
    
    def untrain_positive(self, tokens):
        """for each token, if token in database, decrement the token's counter by 1.
        if token does not exist in the database, pass; if token count == 1, 
        remove from database"""
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN')
        for token in tokens:
            self._decrement_or_remove(token.token_string, polarity='positive')
        self.update_counter('global_counter', value=-1)
        self.update_counter('positive_counter', value=-1)
        # commit to connection
        self.db_connection.commit()
        self.cursor.close()

        return None                

    def untrain_negative(self, tokens):
        """for each token, if token in database, decrement the token's counter by 1.
        if token does not exist in the database, pass; if token count == 1, 
        remove from database"""
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN')
        for token in tokens:
            self._decrement_or_remove(token.token_string, polarity='negative')
        self.update_counter('global_counter', value=-1)
        self.update_counter('negative_counter', value=-1)
        self.db_connection.commit()
        self.cursor.close()
        # close cursor

        return None

    def counter_for_token(self, token, polarity=''):
        if (not polarity) or (polarity not in ['positive', 'negative']):
            return False
        cursor = self.db_connection.cursor()
        try:
            if polarity == 'positive':
                cursor.execute("SELECT count from positive_classification WHERE token=?", (token,))
                current_value = cursor.fetchone()
                if not current_value: # not in database
                    current_value = .5 # using this value as a default; TODO: find optimal value
                else:
                    current_value = current_value[0] # bad form
                print current_value
                return current_value
            else:
                current = cursor.execute("SELECT count from negative_classification WHERE token=?", (token,))
                current_value = cursor.fetchone()
                if not current_value: # not in database; use .5
                    # don't divide by zero
                    current_value = 1 # using this value as a default; TODO: find optimal value
                else:
                    current_value = current_value[0] # bad form
                print current_value
                return current_value
        finally:
            cursor.close()
        return True

    def total_for_polarity(self, polarity=''):
        if (not polarity) or (polarity not in ['positive', 'negative']):
            return False
        cursor = self.db_connection.cursor()
        current_counter = cursor.execute("SELECT counter from counters WHERE name=?", ("%s_counter" % polarity,))
        
        counter_value = current_counter.fetchone()[0]
        if counter_value == 0:
            counter_value = 1
        cursor.close()
        return counter_value

        
