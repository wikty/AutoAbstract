articles = []
df = {}
dc = None

def read_data():
	global articles
	if articles:
		return articles
	with open('data/filelist.txt', 'r', encoding='utf-8') as f:
		filelist = f.readlines()
		for filename in filelist:
			filename = 'data/'+filename.strip()
			with open(filename, 'r', encoding='utf-8') as ff:
				articles.append(ff.read().replace('\n', ''))
	return articles

def get_df():
	global df, dc
	if df:
		return [dc, df]
	with open('data/df.txt', 'r', encoding='utf-8') as f:
		dc = int(f.readline().strip())
		for line in f:
			line = line.strip()
			if line:
				item = line.split(':')
				k = item[0].strip()
				v = item[1].strip()
				if k and v:
					df[k] = int(v)
	return [dc, df]