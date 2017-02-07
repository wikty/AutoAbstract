import math
from tf_idf import get_keywords

def sentence_similarity(sent1, sent2):
	# text rank
	sent1_len = len(sent1)
	sent2_len = len(sent2)
	denominator = math.log(sent1_len) + math.log(sent2_len)
	if denominator < 1e-12:
		return 0.0
	return len(set(sent1) & set(sent2)) / denominator

def article_similarity(art1, art2):
	# cosine distance
	words1 = get_keywords(art1, 20)
	words2 = get_keywords(art2, 20)
	words = set(words1+words2)
	tf1 = {}
	tf2 = {}
	art1 = [word for sentence in art1 for word in sentence]
	art2 = [word for sentence in art2 for word in sentence]
	for word in words:
		if word not in tf1:
			tf1[word] = art1.count(word) / len(art1)
		if word not in tf2:
			tf2[word] = art2.count(word) / len(art2)
	molecular = 0
	n1 = 0
	n2 = 0
	for word in words:
		molecular += tf1[word]*tf2[word]
		n1 += tf1[word]*tf1[word]
		n2 += tf2[word]*tf2[word]
	return molecular/(math.sqrt(n1)*math.sqrt(n2))