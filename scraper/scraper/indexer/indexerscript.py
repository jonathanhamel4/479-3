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
	print "merging docs..."
	dirName = os.path.dirname(os.path.abspath(__file__))
	filePath = join(dirName, 'index/docs.json')
	with open(filePath, 'r') as f:
		docs = json.load(f)

		#info for the document
		docJson = docs.get(str(document_tuple[0]), {})
		docJson["url"] = document_tuple[2]
		docJson["length"] = document_tuple[1]
		docs[str(document_tuple[0])] = docJson

		#info the tf-idf
		previous_length = docs.get("length", 0)
		previous_num_docs = docs.get("numDocs", 0)
		total_length = previous_length + document_tuple[1]
		docs["numDocs"] = previous_num_docs + 1
		docs["length"] = total_length
	with open(filePath, 'w') as f2:
		json.dump(docs, f2, indent=4)


def mergeIndex(partial_index):
	print "merging indexer..."
	dirName = os.path.dirname(os.path.abspath(__file__))
	filePath = join(dirName, 'index/indexer.json')
	with open(filePath, 'r') as f:
		indexer = json.load(f)
		for key in partial_index.keys():
			for doc in partial_index[key].keys():
				tfreqS = partial_index[key][doc] or 0
				indexer[key] = indexer.get(key, {})
				indexer[key][doc] = indexer.get(key).get(doc, 0) + tfreqS
	with open(filePath, 'w') as f2:
		#json.dump(indexer, f2, indent=4)
		json.dump(indexer, f2)

def indexDocument(string_data, doc_id, url):
	string_data = string_data.lower()
	indexer = defaultdict(lambda: defaultdict(int))
	tokenizer = RegexpTokenizer(r'[A-Za-z]+')
	#Get a counter of the terms in a document
	word_tokens = tokenizer.tokenize(string_data)

	token_counter = collections.Counter(word_tokens)
	document_tuple = (doc_id, len(word_tokens), url)
	for tk in token_counter:
		#remove the stopwords
		if tk in set(stopwords.words('english')):
			continue
		indexer[tk][str(doc_id)] = token_counter[tk]
	# save & clear the memory
	mergeIndex(indexer)
	mergeDocumentsDict(document_tuple)
	del document_tuple
	del indexer
	print "Processed: " + str(doc_id) + " at " + url
