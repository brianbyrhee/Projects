from flask import Flask, request, render_template
import re
import click
from .matcher import Text, ExtendedMatch, Matcher
import os
import glob
import math
import logging
import itertools

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask("__name__")

q = ""


def getFiles(path): 
    """ 
    Determines whether a path is a file or directory. 
    If it's a directory, it gets a list of all the text files 
    in that directory, recursively. If not, it gets the file. 
    """

    if os.path.isfile(path): 
        return [path]
    elif os.path.isdir(path): 
        # Get list of all files in dir, recursively. 
        return glob.glob(path + "/**/*.txt", recursive=True)
    else: 
        raise click.ClickException("The path %s doesn't appear to be a file or directory" % path) 

def head(text):
	"""
	Return the first couple of strings in the text for debugging purposes
	"""
	return text[:20]

def sortFreqDict(wordlist):
		"""
		Creates a dictionary with the frequency of words in order of descending frequency.
		That way, you have a higher chance of encountering the desired word in our list created
		from TF-IDF much earlier.
		"""
		wordfreq = [wordlist.count(p) for p in wordlist]
    freqdict =  dict(list(zip(wordlist,wordfreq)))
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

@app.route("/")
def loadPage():
	return render_template('initial.html', query="")

@app.route("/", methods=['POST'])
def cosineSimilarity():
	
	universalSetOfUniqueWords = []
	matchPercentage = 0

	inputQuery = request.form['query']
	if inputQuery:
		lowercaseQuery = inputQuery.lower()
	else:
		#if there is no input Query
		fd = open("querytext.txt", "r")

		#if fd is empty, as assume that it's a path
		if not fd:
			lowercaseQuery = getFiles(text1)
		else:
			lowercaseQuery = fd.read().lower()

	#Replace punctuation by space and split
	queryWordList = re.sub("[^\w]", " ",lowercaseQuery).split()	

	for word in queryWordList:
		if word not in universalSetOfUniqueWords:
			universalSetOfUniqueWords.append(word)

	# check for same constraints
	fd = open("database1.txt", "r")
	if not fd:
		database1 = getFiles(text2)
	else:
		database1 = fd.read().lower()

	#Replace punctuation by space and split
	databaseWordList = re.sub("[^\w]", " ",database1).split()	


  logging.debug('Comparing this/these text(s): %s' % head(database1))
  logging.debug('with this/these text(s): %s' % head(lowercaseQuery))

	for word in databaseWordList:
		if word not in universalSetOfUniqueWords:
			universalSetOfUniqueWords.append(word)

	queryTF = []
	databaseTF = []

	"""
	With the populated list of unique words, we can start building our TF-IDF by keeping track
	of the frequency of each word. Can be improved by using the text.TfidfVectorizer
	class in the sklearn package and NLP libraries. Will implement in the future.
	"""

	for word in universalSetOfUniqueWords:
		queryTfCounter = 0
		databaseTfCounter = 0

		query_dict = sortFreqDict(queryWordList)
		for word2 in queryWordList:
			if word == word2:
				queryTfCounter += 1
		queryTF.append(queryTfCounter)

		data_dict = sortFreqDict(databaseWordList)
		for word2 in databaseWordList:
			if word == word2:
				databaseTfCounter += 1
		databaseTF.append(databaseTfCounter)

	"""
	Calculate the the magnitude of each string converted into a vector. 
	Then we take the cosine of these two vectors and convert it into a probability.
	High cosine similarity equates to high similarity!
	"""

	dotProduct = 0
	for i in range(len(queryTF)):
		dotProduct += queryTF[i]*databaseTF[i]

	queryVectorMagnitude = 0
	for i in range(len(queryTF)):
		queryVectorMagnitude += queryTF[i] ** 2
	queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

	databaseVectorMagnitude = 0
	for i in range(len(databaseTF)):
		databaseVectorMagnitude += databaseTF[i] ** 2
	databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)

	matchPercentage = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100
	constraint = 85
	if matchPercentage <= constraint:
		output = "With a constraint of %0.02f%%, there is no evidence of plagiarism. Change constraint and database for different results"%constraint
	else:
		output = "Input query text matches %0.02f%% with the given database."%matchPercentage

	'''
	print queryWordList
	print
	print databaseWordList
	print queryTF
	print
	print databaseTF
	'''

	return render_template('index.html', query=inputQuery, output=output)

app.run()