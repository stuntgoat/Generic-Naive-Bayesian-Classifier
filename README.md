A Python implementation of a Naive Bayesian Classifier.

Written as generic as possible. The database currently uses Sqlite3 but the NaiveBayesDB can subclassed to use another database if so desired.

Example training usage for spam filtering:
'''
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
'''
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


<div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">generic_token</span> <span style="color: #008000; font-weight: bold">as</span> <span style="color: #0000FF; font-weight: bold">tkn</span> 
<span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">re</span>

<span style="color: #008000; font-weight: bold">class</span> <span style="color: #0000FF; font-weight: bold">SpamTokenizer</span>(<span style="color: #008000">object</span>):
    <span style="color: #BA2121; font-style: italic">&quot;&quot;&quot;parse email content, given as a list of strings- a list of lines in a file.&quot;&quot;&quot;</span>
    <span style="color: #008000; font-weight: bold">def</span> <span style="color: #0000FF">__init__</span>(<span style="color: #008000">self</span>, items):
        <span style="color: #BA2121; font-style: italic">&quot;&quot;&quot;Accepts: a list of email &#39;body&#39; lines.</span>
<span style="color: #BA2121; font-style: italic">        Returns: a list of tokens&quot;&quot;&quot;</span>
        <span style="color: #008000">self</span><span style="color: #666666">.</span>items <span style="color: #666666">=</span> items
        <span style="color: #008000">self</span><span style="color: #666666">.</span>tokens <span style="color: #666666">=</span> []

    <span style="color: #008000; font-weight: bold">def</span> <span style="color: #0000FF">parse_pre_tokens</span>(<span style="color: #008000">self</span>, symbol):
        <span style="color: #BA2121; font-style: italic">&quot;&quot;&quot;remove &#39;=&#39;, &#39;&gt;&lt;&#39;, and any word that does not contain letters; or</span>
<span style="color: #BA2121; font-style: italic">        if the word &#39;spam&#39; occurs, remove that word from the token list. </span>
<span style="color: #BA2121; font-style: italic">        remove cruft from html.&quot;&quot;&quot;</span>
        <span style="color: #008000; font-weight: bold">if</span> (<span style="color: #BA2121">&#39;=&#39;</span> <span style="color: #AA22FF; font-weight: bold">in</span> symbol) <span style="color: #AA22FF; font-weight: bold">or</span> (<span style="color: #BA2121">&#39;&gt;&lt;&#39;</span> <span style="color: #AA22FF; font-weight: bold">in</span> symbol):
            <span style="color: #008000; font-weight: bold">return</span> <span style="color: #008000">None</span>
        spam_in_subject <span style="color: #666666">=</span> re<span style="color: #666666">.</span>compile(<span style="color: #BA2121">&#39;spam&#39;</span>, re<span style="color: #666666">.</span>I)
        <span style="color: #008000; font-weight: bold">if</span> re<span style="color: #666666">.</span>search(spam_in_subject, symbol):
            <span style="color: #008000; font-weight: bold">return</span> <span style="color: #008000">None</span>
        token <span style="color: #666666">=</span> symbol<span style="color: #666666">.</span>rstrip(<span style="color: #BA2121">&quot;&#39;</span><span style="color: #BB6622; font-weight: bold">\&quot;</span><span style="color: #BA2121">(&lt;&gt;*%$#@!:?,.\/&quot;</span>)<span style="color: #666666">.</span>lstrip(<span style="color: #BA2121">&quot;&#39;</span><span style="color: #BB6622; font-weight: bold">\&quot;</span><span style="color: #BA2121">)\/&lt;&gt;*%$#@!?:,.&quot;</span>)
        <span style="color: #008000; font-weight: bold">if</span> re<span style="color: #666666">.</span>search(<span style="color: #BA2121">&quot;[a-zA-Z]{3,}&quot;</span>, token) <span style="color: #AA22FF; font-weight: bold">and</span> (<span style="color: #008000">len</span>(token) <span style="color: #666666">&lt;</span> <span style="color: #666666">13</span>):
            <span style="color: #008000; font-weight: bold">return</span> token
        <span style="color: #008000; font-weight: bold">return</span> <span style="color: #008000">None</span>

    <span style="color: #008000; font-weight: bold">def</span> <span style="color: #0000FF">tokenize</span>(<span style="color: #008000">self</span>):
        <span style="color: #BA2121; font-style: italic">&quot;&quot;&quot;Override this method to process the data_container</span>
<span style="color: #BA2121; font-style: italic">        Returns: this must return a list of Token objects.&quot;&quot;&quot;</span>
        split_tokens <span style="color: #666666">=</span> []
        <span style="color: #008000; font-weight: bold">for</span> item <span style="color: #AA22FF; font-weight: bold">in</span> <span style="color: #008000">self</span><span style="color: #666666">.</span>items:
            split_string <span style="color: #666666">=</span> item<span style="color: #666666">.</span>split()
            split_tokens<span style="color: #666666">.</span>extend(split_string)
        <span style="color: #008000; font-weight: bold">for</span> pre_token <span style="color: #AA22FF; font-weight: bold">in</span> split_tokens:
            t <span style="color: #666666">=</span> <span style="color: #008000">self</span><span style="color: #666666">.</span>parse_pre_tokens(pre_token)
            <span style="color: #008000; font-weight: bold">if</span> t <span style="color: #AA22FF; font-weight: bold">and</span> (t <span style="color: #AA22FF; font-weight: bold">not</span> <span style="color: #AA22FF; font-weight: bold">in</span> <span style="color: #008000">self</span><span style="color: #666666">.</span>tokens):
                <span style="color: #008000">self</span><span style="color: #666666">.</span>tokens<span style="color: #666666">.</span>append(tkn<span style="color: #666666">.</span>Token(t))
        <span style="color: #008000; font-weight: bold">return</span> <span style="color: #008000">self</span><span style="color: #666666">.</span>tokens

                

 
</pre></div>
