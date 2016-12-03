import os
import sys
from os import listdir
from os.path import isfile, join
import re
import xml.etree.ElementTree as ET
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
import json
import collections
from collections import defaultdict

def mergeDocumentsDict(document_tuple):
	print "merging documents"
	# iterate over the smallest document to merge
	# might need to change the directory
	with open('index/docs.json', 'rw') as f:
		docs = json.load(f)
		previous_average = partial_docs.get("avg")
		previous_num_docs = partial_docs.get("numDocs")
		total_length = previous_average * previous_num_docs + document_tuple[1]
		docs["numDocs"] = previous_num_docs + 1
		docs["avg"] = total_length / float(previous_num_docs + 1)
		docs[document_tuple[0]] = partial_docs[document_tuple[0]]
		json.dump(docs, f)

def mergeIndex(partial_index):
	print "merging indexes"
	# iterate over the smallest document to merge
	# might need to change the directory
	with open('index/indexer.json', 'rw') as f:
		indexer = json.load(f)		
		for key in partial_index.keys():
			for doc in partial_index[key].keys():
				tfreqS = partial_index[key][doc] or 0
				indexer[key] = indexer.get(key, {})
				indexer[key][doc] = indexer.get(key).get(doc, 0) + tfreqS
		json.dump(indexer, f)

def indexDocument(string_data, doc_id):
	string_data = stringData.lower()
	indexer = defaultdict(lambda: defaultdict(int))
	tokenizer = RegexpTokenizer(r'[A-Za-z]+')
	#Get a counter of the terms in a document
	word_tokens = tokenizer.tokenize(string_data)
	token_counter = collections.Counter(word_tokens)
	document_tuple = (doc_id, len(word_tokens))
	for tk in token_counter:
		#remove the stopwords
		if tk in set(stopwords.words('english')):
			continue
		frequency = indexer[tk][str(element_id)] or 0
		indexer[tk][str(doc_id)] = frequency + token_counter[tk]
	# save & clear the memory
	mergeIndex(indexer)
	mergeDocumentsDict(document_tuple)
	del documents_dict
	del indexer
	print "Processed: " + str(doc_id)
