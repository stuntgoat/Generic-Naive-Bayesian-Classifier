import sqlite3 as sl3
from os.path import exists
class NaiveBayesDB(object):
    """Creates and maintains a database that will 
    hold values for the NaiveBayesClassifier"""

    def __init__(self, database_path, description=None):
        """Creates the database schema if it 
        the file does not exist"""
        if not exists(database_path):
            self.db = sl3.connect(database_path)        
            # create database
            curser = self.db.curser()
            curser.execute('''create table tokens
                               (token_string text,
                                token_count real)''')
            self.db.commit()
            if description:
                curser.execute('''create table meta
                                   (description text,
                                    container_count integer)''')
                curser.execute('insert into description values (?, 0)', (description,))
                self.db.commit()
                                    

        else:
            self.db = sl3.connect(database_path)
    
    
    # def describe_database(self, decription):
    #     """if not description, set description"""
        
    #     self.db.execute('''create table meta 
    #                        (description text)''')



        
    
