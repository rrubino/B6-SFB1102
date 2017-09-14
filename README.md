# B6-SFB1102
Repository for the B6 project of SFB1102 -- http://www.sfb1102.uni-saarland.de


infodens


# List of Features:

Feature Name | ID | Description | Argument string
--- | --- | --- | ---  
Average word length | 1 | Calculates the average word length per sentence | None
Syllable ratio | 2 | Counting the number of vowel-sequences that are delimited by consonants or space in a word, normalized by the number of tokens in the sentence | None 
Sentence length | 10 | Calculates the length of each sentence in words | None
Lexical density | 3 | The frequency of tokens that are not nouns, adjectives, adverbs or verbs. Computed by dividing the number of tokens not tagged with the given POS tags by the number of tokens in the sentence | 
 Example: 1,NN, c:\textbackslash tagged.txt
1. Flag (0/1) indicating given POS tagged input.
2. List of POS tags (comma separated)
3. POS tagged file path (when flag is 1) 
Lexical richness (type-token ratio) | 11 | The ratio of unique tokens in the sentence over the sentence length | None 
Lexical to tokens ratio | 12 | The ratio of lexical words (given POS tags) to tokens in the sentence | 
   Example: 1,NN, c:\textbackslash tagged.txt
1. Flag (0/1) indicating given POS tagged input.
2. List of POS tags (comma separated)
3. POS tagged file path (when flag is 1) 
Ngram bag of words | 4 | Ngram bag of words | 
   Example: 1,2  (Uni-grams that appear at least twice)
1. N in ngram 
2. Cutoff frequency
Ngram bag of POS | 5 | Ngram bag of POS | 
   Example: 1,2 or 1,2,c:\textbackslash taggedInput.txt  (Uni-grams that appear at least twice)
1. N in ngram 
2. Cutoff frequency
3. Tagged POS input (Optional)
Ngram bag of mixed words | 6 | Ngram bag of mixed words, sentences are tagged and only tags that start with J,N,V, or R are left, the others are actual words (Tagged with NLTK) | 
   Example: 1,2 (Uni-grams that appear at least twice)
1. N in ngram 
2. Cutoff frequency
3. Tagged POS input (Optional)
Ngram bag of lemmas | 7 | Ngram bag of lemmas (lemmatized using NLTK WordNetLemmatizer) | 
   Example: 1,2 (Uni-grams that appear at least twice)
1. N in ngram 
2. Cutoff frequency
3. Tagged POS input (Optional)
Perplexity language model | 17 | Using SRILM's ngram or KenLM to build a language model then compute the sentence scores (log probabilities) and perplexities. | 
   Example: 0,3 (Trigrams language model) or 1,3,models\textbackslash myLM.lm
1. Flag (0/1) Given language model
2. Ngram of the LM and feature
3. Language model file path (if flag is 1) 
