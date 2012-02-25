A Python implementation of a Naive Bayesian Classifier.

Written as generic as possible. The database currently uses Sqlite3 but the NaiveBayesDB can subclassed to use another database if so desired.

Example training usage for spam filtering:

    from naive_bayes_classifier import NaiveBayesClassifier
    from example_tokenizer import SpamTokenizer

    # sqlite3 database file
    SPAM_CLASSIFIER_DB = '/path/to/spam_classifier.db'
    # to train positive:
    spam = SpamTokenizer(raw_data) # process tokens from raw data
    spam.tokenize() # returns a list of tokens 

    # assuming an existing database; see class to add description
    # to the database.
    spam_bayes = NaiveBayesClassifier(SPAM_CLASSIFIER_DB)
    spam_bayes.register_tokens(spam.tokens)
    spam_bayes.train_positive()

    # train negative
    non_spam = SpamTokenizer(non_spam_raw_data)
    non_spam.tokenize()
    spam_bayes.register_tokens(non_spam.tokens)
    spam_bayes.train_negative()

    # Example testing usage, for spam email testing:
    test_email = open('/path/to/test.eml')
    test = SpamTokenizer(test_email)
    test.tokenize()

    spam_bayes.register_tokens(test.tokens)
    spam_bayes.caclulate_probabilities()

    # show results above token list
    print("%.6f positive %.6f negative \n %s \n" % (subject_bayes.sum_positive(),
                                                    subject_bayes.sum_negative(),
                                                    [x.token_string for x in subject_bayes.tokens]))

Background:
Bayes Therom
P(A|B) = (P(B|A)*P(A))/P(B)

The probability of A given B is equal to the probability of B given A multiplied by the probability of A, divided over the probability of B.

A naive bayesian classifier formula

P(S|W) = P(W|S) / ( P(W|S) + P(W|H) )

The probability of a word being spammy, S, given a word, W, is equal to the probability of the frequency of word occurance in all spam messages in the training data, P(W|S)[if there were 300 messages marked spam and 25 occurances of the word 'purchase', the probability would be 25/300=.083], divided by the sum of P(W|S) and the frequency of word occurances in all ham messages in the training data, P(W|H).

Combining individual probabilities

p(S) = (p1 * p2 ... pn) / ( (p1 * p2 ... * pn) + ( (1 - p1) * (1 - p2) ... * (1 - pn) ) )

The formula for summing the probability of a message being labeled as spam, p(S), is equal to the product of each word's probability of being spammy, p1 through pn, divided by the sum of products p1 through pn and the products (1 - p1) through (1 - pn).

Python used to create Sqlite3 database:

    cursor.execute("create table counters (counter INTEGER, name TEXT, description TEXT)")
    cursor.execute("insert into counters VALUES (0, 'global_counter', ?)", (global_description,))
    cursor.execute("insert into counters VALUES (0, 'positive_counter', ?)", (positive_description,))
    cursor.execute("insert into counters VALUES (0, 'negative_counter', ?)", (negative_description,))
    cursor.execute("create table negative_classification (token TEXT UNIQUE, count INTEGER)")
    cursor.execute("create table positive_classification (token TEXT UNIQUE, count INTEGER)")


