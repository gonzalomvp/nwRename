# Adhoc class with a few methods for sequence comparison via Needleman-Wunsch
class Alignment:

	def __init__(self, seq1, seq2, matchScore=2, mismatchScore=-1, gapScore=-1, alignmentType='semi-global'):
		if alignmentType == 'global':
			self.alignmentType = 'global'
			self.trailingGapScore = gapScore
		elif alignmentType == 'semi-global':
			self.alignmentType = 'semi-global'
			self.trailingGapScore = 0
		else:
			raise ValueError('Invalid alignment type')
		self.seq1 = list(seq1)
		self.seq2 = list(seq2)
		self.matchScore = matchScore
		self.mismatchScore = mismatchScore
		self.gapScore = gapScore
		self.alignmentMatrixNumRows = len(seq1)+1
		self.alignmentMatrixNumCols = len(seq2)+1
		self.alignmentMatrix = []
		self.generateAlignmentMatrix()

	def score(self, i, j):
		if (self.seq1[i] == self.seq2[j]):
			return self.matchScore
		else:
			return self.mismatchScore

	def generateAlignmentMatrix(self):
		self.alignmentMatrix = []
		self.alignmentMatrix.append([])
		self.alignmentMatrix[0].append(0)
		for i in xrange(1, self.alignmentMatrixNumRows):
			self.alignmentMatrix.append([])
			self.alignmentMatrix[i].append(i * self.trailingGapScore)
			for j in xrange(1, self.alignmentMatrixNumCols):
				self.alignmentMatrix[0].append(j * self.trailingGapScore)
				self.alignmentMatrix[i].append(max(
					self.alignmentMatrix[i-1][j-1] + self.score(i-1, j-1),
                    self.alignmentMatrix[i][j-1] + self.gapScore,
                    self.alignmentMatrix[i-1][j] + self.gapScore,
				))

	def argmax(self):
		ans = []
		ans.append(self.alignmentMatrixNumRows-1)
		ans.append(self.alignmentMatrixNumCols-1)
		if self.alignmentMatrixNumRows < self.alignmentMatrixNumCols:
			ans[1] = self.alignmentMatrix.index(max(self.alignmentMatrix[ans[0]]))
		else:
			cur = self.alignmentMatrix[0][ans[1]]
			for i in xrange(self.alignmentMatrixNumCols):
				if (self.alignmentMatrix[i][ans[1]] > cur):
					cur = self.alignmentMatrix[i][ans[1]]
					ans[0] = i
		return ans

	def getAlignmentScore(self):
		if self.alignmentType == 'global':
			return self.alignmentMatrix[-1][-1]
		else:
			ij = self.argmax();
			return self.alignmentMatrix[ij[0]][ij[1]]
