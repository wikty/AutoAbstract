from get_data import read_data
from split_sentence import SplitSentence
from split_word import SimpleSplitWord

if __name__ == '__main__':
	articles = read_data()
	articles = [SplitSentence(article).split() for article in articles]
	articles = [[SimpleSplitWord(sentence).split()  for sentence in article ] for article in articles]

	df = {}
	for article in articles:
		words = set()
		for sentence in article:
			words.update(sentence)
		for word in words:
			if word not in df:
				df[word] = 0
			df[word] += 1
	with open('data/df.txt', 'w', encoding='utf-8') as f:
		f.write('{}\n'.format(len(articles)))
		for k in df:
			f.write('{}: {}\n'.format(k, df[k]))