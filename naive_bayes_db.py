import sqlite3 as sl3
from os.path import exists


class NaiveBayesDB(object):
    """Creates and maintains a database that will
    hold values for the NaiveBayesClassifier.
    """
    GLOBAL = 'global_counter'
    POSITIVE = 'positive_counter'
    NEGATIVE = 'negative_counter'
    COUNTERS = set([GLOBAL, POSITIVE, NEGATIVE])

    def __init__(self, database_path):

        """Creates the database schema if the file does not exist"""
        if not exists(database_path):
            self.db_connection = sl3.connect(database_path)
            self.db_connection.text_factory = str
            cursor = self.db_connection.cursor()
            cursor.execute("create table counters (counter INTEGER, name TEXT)")
            cursor.execute("insert into counters VALUES (0, 'global_counter')")
            cursor.execute("insert into counters VALUES (0, 'positive_counter')")
            cursor.execute("insert into counters VALUES (0, 'negative_counter')")
            cursor.execute("create table negative_classification (token BLOB UNIQUE, count INTEGER)")
            cursor.execute("create table positive_classification (token BLOB UNIQUE, count INTEGER)")
            self.db_connection.commit()
            cursor.close()
            return None
        self.db_connection = sl3.connect(database_path)
        self.db_connection.text_factory = str
        self.cursor = None
        return None

    def update_counter(self, counter, value=1):
        """Increment each counter according to train methods."""
        value = int(value)
        if not value:
            print 'invalid integer: %s'
            return False

        if counter not in self.COUNTERS:
            print 'invalid counter'
            return False

        current = self.cursor.execute("SELECT counter from counters WHERE name=?", (counter,))
        current_value = current.fetchone()[0]
        if (current_value == 0) and (value < 1):
            return False
        current_value += value
        self.cursor.execute("UPDATE counters SET counter=? WHERE name=?", (current_value, counter))
        return True

    def _increment_or_insert(self, token, polarity):
        """for each token, if token not in database, add token to the database and set count to 1; if the
        token exists in the database, increment the counter by 1."""
        try:
            if polarity == 'positive':
                self.cursor.execute("insert into positive_classification VALUES (?, ?)", (token, 1))
            elif polarity == 'negative':
                self.cursor.execute("insert into negative_classification VALUES (?, ?)", (token, 1))
        except sl3.IntegrityError:  # token exists in database, so increment token count
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
        except Exception as e:
            print e
            return False

    def _get_count_for_token(self, token, polarity):
        assert polarity in set(['positive', 'negative'])
        if polarity == 'positive':
            self.cursor.execute("SELECT count from positive_classification WHERE token=?", (token,))
        else:
            self.cursor.execute("SELECT count from negative_classification WHERE token=?", (token,))
        # current_cursor
        current_value = self.cursor.fetchone()
        if not current_value:
            return None, 'token not found'
        value = current_value[0]
        return value, None

    def _decrement_positive(self, token):
        value, error = self._get_count_for_token(token, 'positive')
        if error:
            print error
            return

        if value == 1:
            # remove the token from the database instead of setting to 0
            self.cursor.execute("DELETE FROM positive_classification WHERE token=?", (token,))
        else:
            # decrement
            value -= 1
            self.cursor.execute("UPDATE positive_classification SET count=? WHERE token=?", (value, token))
        return True

    def _decrement_negative(self, token):
        value, error = self._get_count_for_token(token, 'negative')
        if error:
            print error
            return

        if value == 1:
            # remove the token from the database instead of setting to 0
            self.cursor.execute("DELETE FROM negative_classification WHERE token=?", (token,))
        else:
            # decrement
            value -= 1
            self.cursor.execute("UPDATE negative_classification SET count=? WHERE token=?", (value, token))
        return True

    def _decrement_or_remove(self, token, polarity):
        """for each token, if token not in database, pass, else if token count >
        1, decrement, else if token count == 1, remove element from database"""
        if polarity not in set([self.POSITIVE, self.NEGATIVE]):
            return False

        try:
            if polarity == 'positive':
                self._decrement_positive(token)
            else:
                self._handle_negative(token)
        except Exception as e:
            print e

        return True

    def train_positive(self, tokens):
        """batch update/insert tokens and increment global and positive counters"""
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN TRANSACTION')
        count = 0
        for token in tokens:
            self._increment_or_insert(token.token_string, 'positive')
            count += 1
        self.update_counter(self.GLOBAL, value=1)
        self.update_counter(self.POSITIVE, value=1)
        self.db_connection.commit()
        self.cursor.close()
        return None

    def train_negative(self, tokens):
        """For each token in tokens, add token/counter and/or increment negative_counter in database.
        Increment the global counter"""
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN TRANSACTION')
        count = 0
        for token in tokens:
            self._increment_or_insert(token.token_string, polarity='negative')
            count += 1
        self.update_counter('global_counter', value=count)
        self.update_counter('negative_counter', value=count)
        self.db_connection.commit()
        self.cursor.close()

    def untrain_positive(self, tokens):
        """for each token, if token in database, decrement the token's counter by 1.
        if token does not exist in the database, pass; if token count == 1,
        remove from database"""
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN')
        count = 0
        for token in tokens:
            self._decrement_or_remove(token.token_string, polarity='positive')
            count -= 1
        self.update_counter('global_counter', value=count)
        self.update_counter('positive_counter', value=count)
        self.db_connection.commit()
        self.cursor.close()

    def untrain_negative(self, tokens):
        """for each token, if token in database, decrement the token's counter by 1.
        if token does not exist in the database, pass; if token count == 1,
        remove from database"""
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('BEGIN')
        count = 0
        for token in tokens:
            res = self._decrement_or_remove(token.token_string, polarity='negative')
            if res:
                count -= 1
        self.update_counter(self.GLOBAL, value=count)
        self.update_counter(self.NEGATIVE, value=count)
        self.db_connection.commit()
        self.cursor.close()

    def counter_for_token(self, token, polarity):
        if polarity not in set(['positive', 'negative']):
            print 'polarity not found: %s' % polarity
            return
        value, error = self._get_count_for_token(token, polarity)
        if error:
            print error
            return

        return value

    def total_for_polarity(self, polarity):
        """Returns the counter for the given polarity"""
        if polarity not in set(['positive', 'negative']):
            return False
        cursor = self.db_connection.cursor()
        current_counter = cursor.execute("SELECT counter from counters WHERE name=?", ("%s_counter" % polarity,))
        counter_value = current_counter.fetchone()[0]
        if counter_value == 0:
            counter_value = 1
        cursor.close()
        return counter_value
