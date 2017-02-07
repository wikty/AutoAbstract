import networkx
import numpy

from similarity import sentence_similarity

class TextRank(object):
	def __init__(self, sentences):
		self.sentences = sentences
		self.len = len(sentences)

	def rank(self):
		matrix = numpy.zeros((self.len, self.len))
		for i in range(0, self.len):
			for j in range(i, self.len):
				similarity = sentence_similarity(self.sentences[i], self.sentences[j])
				matrix[i, j] = matrix[j, i] = similarity
		graph = networkx.from_numpy_matrix(matrix)
		rank_dict = networkx.pagerank(graph)
		sentences = []
		for index, score in rank_dict.items():
			sentences.append({
				'index': index,
				'score': score,
				'sentence': self.sentences[index]
			})
		return sorted(sentences, reverse=True, key=lambda item: item['score'])