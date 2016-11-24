.. infodens documentation master file, created by
   sphinx-quickstart on Wed Nov 23 13:50:33 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to infodens's documentation!
====================================

.. toctree::
   :maxdepth: 2
   
   .. :ref:`search`

Using the API
=============

About the software
------------------

This is a machine learning package for translationese detection experiments. It has  often  been  observed  that  the 
product  of  translation  is  somehow  different than non-translated text, scholars have emphasized  two  distinct  bases  for  such  differences. 
While some point to the interference from the source language  spilling  over  into  translation  in  a source language specific   way,   others 
have  noted  general  effects  of  the  process  of translation that are independent of source language.

In this software, we implement various features and machine learning algorithms to experiment on text documents (Original and Translated).
Machine learning algorithms implemented include:
 
 * Support Vector Machines (SVM)
 * Neural Networks
 * Decision Trees
 * Random Forests
 
Features implemented include:
 
 * surface features:
  - average word length
  - sentence length
  - syllable ratio
 * lexical features:
 	- lexical density
 	- lexical richness
 	- parse tree depth
 * ngram features
  - Bag-of-word ngrams
  - Bag-of-POS ngrams
  - Bag-of-lemma ngrams
  - Bag-of-MixedWords ngrams
  
 	



Downloading the software
------------------------

Goto any *directory* of your choice:

	* cd path/to/directory
Clone the software:

	* git clone https://github.com/rrubino/B6-SFB1102.git


Running the software
------------------------
Goto your chosen *directory*:

	* cd path/to/directory
Run the software:

	* python main.py
	
	
Pre-requisites
---------------

	* Python programming language
	* Natural Language ToolKit
	* Scikit
	* Pattern Library


Configuration
--------------
This is where you set the parameters (features, classifiers etc.) for running the program
Open the tesconfig.txt using a text editor (e.g. gedit textconfig.txt)

| Find the line that starts with “**input files** :”. On this line you are to input two file paths. The first path is the path to the file containing the sentences (original and translated) for training and testing and the second path is the path containing the labels or classes of the sentences.
input files : path/to/sentences.txt path/to/classes.txt

| Find the line that starts with “**output classifier** :”. On this line you are to input a path which would be a path to a file that would contain results of the classification (Accuracy, precision, recall and fscore).
output classifier: path/to/classificationResults.txt

| Find the line that starts with “**classifiers** :”. On this line you will input the names of the classifiers you intend to experiment with separated by spaces.
| classifiers : DecisionTree RandomForest SVM
You must input at least one of these. But which one of them and how many you choose is up to you

| On the line that starts with “**language model**:” you are to input a path to a file that contains sentences from which you intend to create a language model which you might need for some feature extraction modules.
language model: path/to/file.txt


Features Configuration
~~~~~~~~~~~~~~~~~~~~~~

| 1. **averageWordLength**:
| **Description**: Mean length of words (in characters) based on the assumption that translated texts used simpler words, particularly shorter ones.
| **Parameters**: None. This feature takes no parameter. To configure, just type the feature id 1

| 2. **syllableRatio**:
| **Description**: We approximate this feature by counting the number of vowel-sequences that are delimited by consonants or space in a word, normalized by the number of tokens in the chunk.
| **Parameters**: None. This feature also takes no parameter. To configure, just type the feature id 2

| 3. **lexicalDensity**:
| **Description**: The frequency of tokens that are not nouns, adjectives, adverbs or verbs. This is computed by dividing the number of tokens tagged with POS tags that do not start with J, N, R or V by the number of tokens in the chunk
| **Parameters**: JJ,NN,VP. POS tags that start with J, N, R, or V
| **Configure**: 3 JJ,NN,VP,VB

| 4. **ngramBagOfWords**:
| **Description**: Extracts n-gram bag of words features.
| **Parameters**: n,minimumFrequency. The first parameter is the size of the ngrams n, the second is the minmum frequency required to include a token in the ngram construction
| **Configure**: 4 2,10

| 5. **ngramPOSBagOfWords**:
| **Description**: Extracts n-gram bag of words features for POS tags.
| **Parameters**: n,minimumFrequency. The first parameter is the size of the ngrams n, the second is the minmum frequency required to include a token in the ngram construction
| **Configure**: 5 2,10

| 6. **ngramMixedBagOfWords**:
| **Description**: Extracts n-gram bag of words features for Mixed Words (Function words replaced by POS).
| **Parameters**: n,minimumFrequency. The first parameter is the size of the ngrams n, the second is the minmum frequency required to include a token in the ngram construction
| **Configure**: 6 2,10


| 7. **ngramLemmaBagOfWords**:
| **Description**: Extracts n-gram bag of words features for word lemmas.
| **Parameters**: n,minimumFrequency. The first parameter is the size of the ngrams n, the second is the minmum frequency required to include a token in the ngram construction
| **Configure**: 7 2,10

| 8. **parseTreeDepth**:
| **Description**: Find depth of a sentence's parse tree
| **Parameters**: None. This feature also takes no parameter. To configure, just type the feature id 8

| 9. N/A
| 10. **sentenceLength**:
| **Description**: Computes sentences’ length as a feature
| **Parameters**: None. This feature also takes no parameter. To configure, just type the feature id 10

| 11. **lexicalRichness**:
| **Description**: The ratio of unique tokens in the sentence over the sentence length.
| **Parameters**: None. This feature also takes no parameter. To configure, just type the feature id 11

| 12. **lexicalToTokens**: Description: The ratio of lexical words to tokens in the sentence.
| **Parameters**: CC,DT,WDT,IN,PDT
| **Configure**: 12 CC,DT,WDT,IN,PDT
