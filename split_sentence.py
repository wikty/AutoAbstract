import re

class SimpleSplitSentence(object):
	def __init__(self, raw):
		self.raw = raw
		self.delimiter_regex = r'。'

	def remove_newline(self, raw):
		s = set('\n\r\t')
		p = []
		for char in raw:
			if char not in s:
				p.append(char)
		return ''.join(p)

	def split(self):
		raw = self.remove_newline(self.raw)
		sentences = re.split(self.delimiter_regex, raw)
		return [sentence.strip() for sentence in sentences if sentence.strip()]

class SplitSentence(object):
	def __init__(self, raw):
		self.raw = raw
		self.delimiter = set("。！？")
		self.punctuation_pair = set('《》“”‘’{}（）()【】""')
		self.punctuation_pair_prefix = {
			'《': '》',
			'“': '”',
			'‘': '’',
			'【': '】',
			'（': '）',
			'(': ')',
			'{': '}',
			'"': '"'
		}
		self.punctuation_pair_suffix = {
			'》': '《',
			'”': '“',
			'’': '‘',
			'】': '【',
			'）': '（',
			')': '(',
			'}': '{',
			'"': '"'
		}
		self.punctuation_pair_stack = []

	def split(self):
		sentences = []
		sentence = []
		last_char = ''
		for char in self.raw:
			sentence.append(char)

			if char in self.punctuation_pair_prefix:
				self.punctuation_pair_stack.append(char)
			elif char in self.punctuation_pair_suffix:
				prefix = self.punctuation_pair_suffix[char]
				index = 0
				for i in range(len(self.punctuation_pair_stack)-1, -1, -1):
					if self.punctuation_pair_stack[i] == prefix:
						index = i
						break
				self.punctuation_pair_stack = self.punctuation_pair_stack[:index]
			elif char in self.delimiter and len(self.punctuation_pair_stack)==0:
				sentences.append(''.join(sentence))
				sentence = []
		return sentences