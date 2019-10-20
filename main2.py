import string
import csv
import math

# EXERCISE 2.1
# NON FUNZIONA, URGE MODIFICARE TOTO UFF
dataset = [ [], [] ]
with open("imDB.txt", encoding='utf-8') as f:
    for row in csv.reader(f):
        dataset[0].append(row[0].replace("<br /><br />", " ")) # Delete "" from the dataset
        dataset[1].append(row[1])
# pop
dataset[0].pop(0)
dataset[1].pop(0)

# EXERCISE 2.2
# Compute the tokens for each document.
# Input: a list of strings. Each item is a document to tokenize.
# Output: a list of lists. Each item is a list containing the tokens of the
# relative document.
def tokenize(docs):
    tokens = []
    for doc in docs:
        for punct in string.punctuation:
            doc = doc.replace(punct, " ")
            split_doc = [token.lower() for token in doc.split(" ") if token]
            tokens.append(split_doc)
    return tokens

def termFrequency(doc):
    # list of all dictionary
    listOfDictionary = []
    tokens = tokenize(doc)
    for el in tokens:
        dictionary = {} # empty dictionary for each doc
        for word in el:
            if str(word) not in dictionary.keys():
                number = el.count(word)
                dictionary[str(word)] = str(number)
        listOfDictionary.append(dictionary)
    return listOfDictionary

# term frequency of the first 2 document
x = [dataset[0][0], dataset[0][1]]
list = termFrequency(x)
for el in list:
    for k, v in el.items():
        print(f"{k}: {v}")


# EXERCISE 2.4
print("\nFREQUENCY")
def document_frequency(token):
    counter = 0
    for document in dataset[0]:
        if document.find(str(token)) != -1:
            counter += 1
    return counter

# go function
print("DF: "+str(document_frequency("point")))

def inverse_document_frequency(token):
    df = document_frequency(token)
    n = len(dataset[1])
    if df != 0:
        inverse_df = math.log10((n/df))
    else:
        inverse_df = 0
    return inverse_df

# go function
print("IDF: "+str(inverse_document_frequency("point")))

# EXERCISE 2.5
print("\nIDF-DF frequency:")
def id_idf(tokens):
    # empty dictionary
    dictionary_id_idf = {}

    for token in tokens:
        weight = inverse_document_frequency(token) * document_frequency(token)
        dictionary_id_idf[str(token)] = weight
    return dictionary_id_idf

# go function
example = ["for", "point"]
dic = id_idf(example)
for k, v in dic.items():
    print(f"{k}: {v}")

# EXERCISE 6
def norm(d):
    """Compute the L2-norm of a vector representation."""
    return sum([ tf_idf**2 for t, tf_idf in d.items() ])**.5

def dot_product(d1, d2):
    """Compute the dot product between two vector representations."""
    word_set = set(list(d1.keys()) + list(d2.keys()))
    return sum([( d1.get(d, 0.0) * d2.get(d, 0.0)) for d in word_set ])

def cosine_similarity(d1, d2):
    """
    Compute the cosine similarity between documents d1 and d2.
    Input: two dictionaries representing the TF-IDF vectors for documents
    d1 and d2.
    Output: the cosine similarity.
    """
    return dot_product(d1, d2) / (norm(d1) * norm(d2))

# first document
def positive_or_negative(index):

    upDoc = [docs for docs, value in zip(dataset[0], dataset[1]) if int(value) == 1]
    downDoc = [docs for docs, value in zip(dataset[0], dataset[1]) if int(value) == 0]

    # positive documents
    upTokens = tokenize(upDoc)
    upWeight = id_idf(upTokens)

    # negative documents
    downTokens = tokenize(downDoc)
    downWeight = id_idf(downTokens)

    # document to test
    test = dataset[0][int(index)]

    upPoints = sum([ cosine_similarity(test, doc) for doc in upWeight ])/len(upDoc) #mean value
    downPoints = sum([ cosine_similarity(test, doc) for doc in downWeight ])/len(downDoc) #mean value

    if upPoints > downPoints:
        return 1
    elif upPoints < downPoints:
        return 0
    else:
        print("Not able to distinguish if positive or negative...")
        return -1

# go function
print("\nCosine similarity")
print("Document 1 : "+ str(positive_or_negative(0)))