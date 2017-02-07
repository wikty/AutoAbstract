import json
from split_sentence import SimpleSplitSentence, SplitSentence
from split_word import SimpleSplitWord
from text_rank import TextRank
from extract_abstract import text_rank_extract_abstract
from get_data import read_data, get_df
from tf_idf import get_keywords
from similarity import article_similarity
from extract_word import SimpleExtractor

def test_split_sentence(raw):
	spliter1 = SimpleSplitSentence(raw)
	spliter2 = SplitSentence(raw)
	return spliter2.split()

def test_split_word(raw):
	spliter = SimpleSplitWord(raw)
	return spliter.split()

def test_text_rank(sentences):
	ranker = TextRank(sentences)
	return ranker.rank()

def test_extract_abstract_by_text_rank(sentences, k=5):
	return text_rank_extract_abstract(sentences, k)

def test_article_similarity(art1, art2):
	return article_similarity(art1, art2)

if __name__ == '__main__':
	# articles = read_data()
	# sentences = test_split_sentence(articles[0])
	# sentences = [test_split_word(sentence) for sentence in sentences]
	#print(test_text_rank(sentences))
	#print(test_extract_abstract_by_text_rank(sentences))

	# with open('input.txt', 'w', encoding='utf-8') as f:
	# 	f.write(articles[0])
	# with open('output.txt', 'w', encoding='utf-8') as f:
	# 	f.write(test_extract_abstract_by_text_rank(sentences))
	#print(get_keywords(sentences))

	# sentences1 = test_split_sentence(articles[1])
	# sentences1 = [test_split_word(sentence) for sentence in sentences1]

	#print(test_article_similarity(sentences, sentences1))
	articles = read_data()
	with open('test.txt', 'w', encoding='utf-8') as f:
		extractor = SimpleExtractor(articles[0])
		f.write(json.dumps(extractor.get_suffix(), ensure_ascii=False))
		f.write('\n')
		f.write(json.dumps(extractor.get_reverse_suffix(), ensure_ascii=False))
		f.write('\n')
		f.write(json.dumps(extractor.get_term_freq(), ensure_ascii=False))
		f.write('\n')
		f.write(json.dumps(extractor.extract(), ensure_ascii=False))