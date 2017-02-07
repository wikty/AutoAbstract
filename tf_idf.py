import math
from get_data import get_df

def get_keywords(article, k=100):
	[dc, df] = get_df()
	words = set()
	word_count = {}
	keywords = []
	for sentence in article:
		words.update(sentence)
		for word in sentence:
			if word not in word_count:
				word_count[word] = 0
			word_count[word] += 1
	for word in words:
		document_freq = df.get(word, 0) + 1
		term_freq = word_count[word]
		score = term_freq * math.log(dc/document_freq)
		keywords.append([word, score])
	keywords = sorted(keywords, reverse=True, key=lambda item: item[1])[:k]
	return [keyword[0].strip() for keyword in keywords if keyword[0].strip()]