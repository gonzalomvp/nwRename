class Scores:
	def __init__(self, match=2, miss=-1, gap=-1, edge=-1):
		self.match = match
		self.miss = miss
		self.gap = gap
		self.edge = edge

def score(scores, a, b):
	return scores.match if a == b else scores.miss

def generateAM(scores, s1, s2):
	am = [[0 if j == 0 else j * scores.edge for j in xrange(len(s2)+1)]]
	for i in xrange(1, len(s1)+1):
		am.append([])
		am[i].append(i * scores.edge)
		for j in xrange(1, len(s2)+1):
			am[i].append(max(
				am[i-1][j-1] + score(scores, s1[i-1], s2[j-1]),
				am[i][j-1] + scores.gap,
				am[i-1][j] + scores.gap,
			))
	return am

def argmax(am):
	i, j = len(am)-1, len(am[0])-1
	if len(am) >= len(am[0]):
		col = [am[i][-1] for i in xrange(len(am))]
		i =  col.index(max(col))
	else:
		j = am[-1].index(max(am[-1]))
	return i, j

def getAlignmentScore(scores, am):
	if scores.edge == 0: # Semi-global
		i, j = argmax(am)
		return am[i][j]
	else:
		return am[-1][-1]
