import jieba

class SimpleSplitWord(object):
	def __init__(self, sentence):
		self.sentence = sentence

	def split(self):
		return list(jieba.cut(self.sentence))