import re, sys, string

from collections import defaultdict
from math import log

###################################
# Input: word
# Output: word without punctuation
###################################
def cleanPunctuation(word):
    clean_regex = re.compile('[%s]' % re.escape(string.punctuation))
    return clean_regex.sub('', word.lower())

###################################
# Input: doc
# Output: vocab_bag (from doc)
###################################
def getVocab(doc):
    vocab_bag = set()
    for each in doc:
        for single in each.split()[:-1]:
            vocab_bag.add(cleanPunctuation(single))

    return vocab_bag

###################################
# Input: existing_txt (trainingSet vs testSet) new_txt (output file name)
# Output: vocab (set) documents (list)
###################################
def preProcessingStep(existing_txt, new_txt):
    documents = []
    read_txt = open(existing_txt, 'r')
    split_lines = read_txt.read().splitlines()
    for each in split_lines:
        word_list = []
        for word in each.split():
            new_word = cleanPunctuation(word)
            word_list.append(new_word)
        documents.append((word_list[:-1], int(each.split()[-1])))
    vocab = getVocab(split_lines)
    vocab.discard('')
    read_txt.close()

    write_txt = open(new_txt, 'w')
    corrected_documents = []
    for each in documents:
        feature_vector = []
        for word in vocab:
            if word in each[0]:
                feature_vector.append('1')
            else:
                feature_vector.append('0')
        corrected_documents.append((','.join(feature_vector) + ',' + str(each[1])))
    write_txt.write(','.join(sorted(list(vocab))) + '\n' + '\n'.join(corrected_documents))
    write_txt.close()
    return vocab, documents

###################################
# Input: vocab (set) documents (list) bool_check (list)
# Output: count (dict) percentage (defaultdict (same as dict just with default key))
###################################
def training(vocab, documents, bool_check):
    total, count, percentage = {}, {}, defaultdict(dict)
    for each in bool_check:
        bool_count = 0
        for doc in documents:
            if doc[1] == each:
                bool_count += 1
        total_count = len(documents)
        count[each] = log(bool_count / total_count)
        
        dirty = []
        clean = lambda l: [item for sublist in l for item in sublist]
        for doc in documents:
            if doc[1] == each:
                dirty.append(doc[0])
        total[each] = clean(dirty)
        sum_total = sum([total[each].count(w) for w in vocab])

        for word in vocab:
            word_count = total[each].count(word)
            percentage[word][each] = log((word_count + 1) / (sum_total + 1))

    return count, percentage

###################################
# Input: document (list) count (dict) percentage (defaultdict) bool_check (list) vocab (set)
# Output: max (largest item)
###################################
def testing(document, count, percentage, bool_check, vocab):
    prob, word_list = {}, []
    for word in document[0]:
        if word in vocab:
            word_list.append(word)

    for each in bool_check:
        prob[each] = count[each]
        for word in word_list:
            prob[each] = prob[each] + percentage[word][each]

    return max(prob.keys(), key=(lambda key: prob[key]))

###################################
# Input: results (list) test_docs  train_doc (string) test_doc (string)
# Output: N/A
###################################
def analyzeOutput(results, test_docs, train_doc, test_doc):
    wrong = []
    for result, doc in zip(results, test_docs):
        if result != doc[1]:
            wrong.append(doc + tuple([result]))

    correct = len(test_docs) - len(wrong)
    accuracy = correct / len(test_docs)
    results = """####################################
Result Accuracy:   %s%%
Test Document:     %s
Training Document: %s
####################################""" % (int(round(accuracy * 100,0)), test_doc, train_doc)
    print(results)

###################################
# Input: train_doc (string) test_doc (string)
# Output: vocab (set) documents (list) test_documents (list)
###################################
def setUpTrain(train_doc, test_doc): 
    vocab, documents = preProcessingStep(train_doc, 'preprocessed_train.txt')
    _, test_documents = preProcessingStep(test_doc, 'preprocessed_test.txt')
    return vocab, documents, test_documents

###################################
# Input: test_docs (list) count (dict) percentage (defaultdict) bool_check (list) vocab (set) train_doc (string) test_doc (string)
# Output: N/A
###################################
def test(test_docs, count, percentage, bool_check, vocab, train_doc, test_doc):
    results = []
    for doc in test_docs:
        results.append(testing(doc, count, percentage, bool_check, vocab))
    analyzeOutput(results, test_docs, train_doc, test_doc)


if __name__ == '__main__':
    bool_check = [0, 1]
    sys.stdout = open('results.txt', 'wt')

    vocab, documents, test_documents = setUpTrain('trainingSet.txt', 'trainingSet.txt')
    count, percentage = training(vocab, documents, bool_check)
    test(documents, count, percentage, bool_check, vocab, 'trainingSet.txt','trainingSet.txt')

    vocab, documents, test_documents = setUpTrain('trainingSet.txt', 'testSet.txt')
    count, percentage = training(vocab, documents, bool_check)
    test(test_documents, count, percentage, bool_check, vocab, 'trainingSet.txt','testSet.txt')
