import math

class SimpleExtractor(object):
	def __init__(self, raw, word_len_max=5, term_freq_max=0.01, neighbour_entropy_max=0.5, cluster_degree_max=5):
		self.raw = raw
		reverse_raw = raw[::-1]
		self.reverse_raw = reverse_raw
		self.word_len_max = word_len_max
		raw_len = len(raw)
		index_list = []
		for word_len in range(1, word_len_max+1):
			l = []
			for start in range(0, raw_len-word_len+1):
				l.append([start, min(start+word_len, raw_len)])
			index_list.append(l)
		self.suffix_list = []
		self.reverse_suffix_list = []
		for word_len in range(1, word_len_max+1):
			l = sorted(index_list[word_len-1], key=lambda item: raw[item[0]:item[1]])
			self.suffix_list.append(l)
			l = sorted(index_list[word_len-1], key=lambda item: reverse_raw[item[0]:item[1]])
			self.reverse_suffix_list.append(l)
		self.term_freq_max = term_freq_max
		self.neighbour_entropy_max = neighbour_entropy_max
		self.cluster_degree_max = cluster_degree_max

	def get_suffix(self):
		r = []
		for word_len in range(1, self.word_len_max+1):
			r.append([self.raw[start:end] for start, end in self.suffix_list[word_len-1]])
		return r

	def get_reverse_suffix(self):
		r = []
		for word_len in range(1, self.word_len_max+1):
			r.append([self.reverse_raw[start:end] for start, end in self.reverse_suffix_list[word_len-1]])
		return r

	def get_term_freq(self):
		term_freq = {}
		total_term = 0
		for i in range(0, self.word_len_max-1):
			suffix_list = self.suffix_list[i]
			next_suffix_list = self.suffix_list[i+1]
			reverse_suffix_list = self.reverse_suffix_list[i]
			next_reverse_suffix_list = self.reverse_suffix_list[i+1]
			for start, end in suffix_list:
				term = self.raw[start:end]
				if term not in term_freq:
					total_term += 1
					term_freq[term] = {
						'count': 0,
						'left_freq': {},
						'right_freq': {},
						'left_freq_sum': 0,
						'right_freq_sum': 0
					}
					for j in range(0, len(next_suffix_list)):
						s = next_suffix_list[j][0]
						e = next_suffix_list[j][1]
						next_term = self.raw[s:e]
						if next_term.startswith(term):
							if next_term[-1] not in term_freq[term]['right_freq']:
								term_freq[term]['right_freq'][next_term[-1]] = 0
							term_freq[term]['right_freq'][next_term[-1]] += 1
							term_freq[term]['right_freq_sum'] += 1
						s = next_reverse_suffix_list[j][0]
						e = next_reverse_suffix_list[j][1]
						prev_term = self.reverse_raw[s:e]
						if prev_term.startswith(term[::-1]):
							if prev_term[-1] not in term_freq[term]['left_freq']:
								term_freq[term]['left_freq'][prev_term[-1]] = 0
							term_freq[term]['left_freq'][prev_term[-1]] += 1
							term_freq[term]['left_freq_sum'] += 1
				term_freq[term]['count'] += 1
		return [term_freq, total_term]

	def extract(self):
		term_list = []
		[term_freq, total_term]= self.get_term_freq()
		for term in term_freq:
			right_entropy = 0.0
			left_entropy = 0.0
			tf = term_freq[term]['count']
			if term_freq[term]['right_freq_sum']:
				for right_term in term_freq[term]['right_freq']:
					p = term_freq[term]['right_freq'][right_term]/term_freq[term]['right_freq_sum']
					right_entropy -= p * math.log(p)
			if term_freq[term]['left_freq_sum']:
				for left_term in term_freq[term]['left_freq']:
					p = term_freq[term]['left_freq'][left_term]/term_freq[term]['left_freq_sum']
					left_entropy -= p * math.log(p)
			#neighbour_entropy = min(right_entropy, left_entropy)
			if right_entropy > 1e-12 and left_entropy > 1e-12:
				neighbour_entropy = min(right_entropy, left_entropy)
			else:
				neighbour_entropy = max(right_entropy, left_entropy)
			l = []
			for i in range(1, len(term)):
				part1 = term[:i]
				part2 = term[i:]
				p = (total_term*term_freq[term]['count'])/(term_freq[part1]['count']*term_freq[part2]['count'])
				if p > 1e-12:
					l.append(p)
			cluster_degree = min(l) if l else 0
			term_list.append([term, tf/total_term, neighbour_entropy, cluster_degree])
		return list(filter(lambda item: item[1]>self.term_freq_max and item[2]>self.neighbour_entropy_max and item[3]>self.cluster_degree_max, term_list))