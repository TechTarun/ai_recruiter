from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, PorterStemmer
import string

class PreProcessor():
  SPECIAL_SYMBOLS = '·'
  STANDARD_PUNCTUATIONS = string.punctuation
  PUNCTUATIONS = SPECIAL_SYMBOLS + STANDARD_PUNCTUATIONS
  STOP_WORDS = set(stopwords.words('english'))

  def tokenize(self, string):
    raw_tokens = word_tokenize(string)
    return raw_tokens

  def filter_out(self, type, tokenlist):
    cleaned_tokens = []
    # remove punctuation symbols from tokens
    if 'punctuation' in type.lower():
      for token in tokenlist:
        if token not in self.PUNCTUATIONS:
          cleaned_tokens.append(token)
    
    # remove stop words from tokens
    elif 'stopwords' in type.lower():
      for token in tokenlist:
        if token not in self.STOP_WORDS:
          cleaned_tokens.append(token)

    # remove both punctuations and stop words
    elif 'total' in type.lower():
      for token in tokenlist:
        if token not in self.STOP_WORDS and token not in self.PUNCTUATIONS and token.isalpha():
          cleaned_tokens.append(token)
    return cleaned_tokens

  def stemmize_tokens(self, tokenlist):
    # stemmer = SnowballStemmer(language='english')
    stemmer = PorterStemmer()
    stemmed_tokens = []
    for token in tokenlist:
      stemmed_tokens.append(stemmer.stem(token))
    return stemmed_tokens

  def downcase_to_set(self, tokenList):
    result_set = set([ele.lower() for ele in tokenList])
    return result_set

#
# -----------Sample usage-----------
# prep = PreProcessor()
# raw_tokens = prep.tokenize("· BS in Computer Science or related technical field (In lieu of degree, 5 years of relevant work experience). · 3+ years of experience in software development. · 2+ years of rich, hands-on programming experience in Java, C++, or other object-oriented languages. Familiarity with one or more of: Python, Perl, PHP. · 2+ years of experience with OO design and common design patterns. · Expertise in data structures, algorithms, and complexity analysis. The ability to produce bullet-proof code that is fault-tolerant, efficient and maintainable. · Academic and/or industry experience with one of more of the following domains: computer vision, image recognition, machine learning or distributed systems. · Strong examples demonstrating past work experience, deliverables and/or innovation across a broad range of methods.")
# clean_tokens = prep.filter_out('punctuations', raw_tokens)
# cleaner_tokens = prep.filter_out('stopwords', clean_tokens)
# stemmed_tokens = prep.stemmize_tokens(cleaner_tokens)
# print(stemmed_tokens)
#