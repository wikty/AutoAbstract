import random
from split_sentence import SplitSentence
from split_word import SimpleSplitWord
from text_rank import TextRank
from get_data import read_data
from tf_idf import get_keywords

def text_rank_extract_abstract(sentences, k=5):
	ranker = TextRank(sentences)
	rank_list = ranker.rank()[:k]
	rank_list = sorted(rank_list, key=lambda item: item['index'])
	return '\n'.join([''.join(item['sentence']) for item in rank_list])

def cluster_extract_abstract(sentences, k=5):
	rank_list = []
	keywords = set(get_keywords(sentences))
	for sentence in sentences:
		rank_list.append([sentence, len(keywords-set(sentence))])
	rank_list = sorted(rank_list, reverse=True, key=lambda item: item[1])[:k]
	return '\n'.join([''.join(item[0]) for item in rank_list])

if __name__ == '__main__':
	articles = read_data()
	index = random.randint(0, len(articles)-1)
	sentences = SplitSentence(articles[index]).split()
	sentences = [SimpleSplitWord(sentence).split() for sentence in sentences]
	abstracts = text_rank_extract_abstract(sentences)

	with open('test.txt', 'w', encoding='utf-8') as f:
		f.write(articles[index])
		f.write('\n\n\n')
		f.write(abstracts)
	#print()
	
	#print(cluster_extract_abstract(sentences))