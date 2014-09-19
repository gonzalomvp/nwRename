# Some constants
GAP_SYMBOL = '-'
MATCH_SYMBOL = '='
MISMATCH_SYMBOL = '!'

# Adhoc class with a few methods for sequence comparison via Needleman-Wunsch
class Alignment:

	def __init__(self, seq1, seq2, matchScore=2, mismatchScore=-1, gapScore=-1):
		self.seq1 = list(seq1)
		self.seq2 = list(seq2)
		self.isAligned = False
		self.hasBeenScored = False
		self.matchScore = matchScore
		self.mismatchScore = mismatchScore
		self.gapScore = gapScore
		self.alignmentMatrixNumRows = len(seq1)+1
		self.alignmentMatrixNumCols = len(seq2)+1
		self.alignmentMatrix = []
		self.traceback = []
		self.cmp = ''
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
			self.alignmentMatrix[i].append(i * self.mismatchScore)
			for j in xrange(1, self.alignmentMatrixNumCols):
				self.alignmentMatrix[0].append(j * self.mismatchScore)
				self.alignmentMatrix[i].append(max(
					self.alignmentMatrix[i-1][j-1] + self.score(i-1, j-1),
                    self.alignmentMatrix[i][j-1] + self.gapScore,
                    self.alignmentMatrix[i-1][j] + self.gapScore,
				))

	def minScore(self):
		return max(self.alignmentMatrixNumRows, 
			self.alignmentMatrixNumCols)*min(self.mismatchScore, self.gapScore)

	# TODO: Review this
	def align(self):
		i, j = self.alignmentMatrixNumRows-1, self.alignmentMatrixNumCols-1
		self.traceback = [[i, j]]
		minimum = self.minScore()
		compliants = [minimum, minimum, minimum]
		while i > 0 or j > 0:
			if i > 0 and j > 0 and self.alignmentMatrix[i][j] == self.alignmentMatrix[i-1][j-1] + self.score(i-1, j-1):
				compliants[0] = self.alignmentMatrix[i-1][j-1]
			if i > 0 and self.alignmentMatrix[i][j] == self.alignmentMatrix[i-1][j] + self.gapScore:
				compliants[1] = self.alignmentMatrix[i-1][j]
			if j > 0 and self.alignmentMatrix[i][j] == 	self.alignmentMatrix[i][j-1] + self.gapScore:
				compliants[2] = self.alignmentMatrix[i][j-1]

			highest = max(compliants)

			if i > 0 and j > 0 and highest == self.alignmentMatrix[i-1][j-1]:
				self.traceback.append([i,-1, j-1])
				i -= 1
				j -= 1
			elif i > 0 and highest == self.alignmentMatrix[i-1][j]:
				self.traceback.append([i-1, j])
				self.seq2.insert(j, GAP_SYMBOL)
				i -= 1
			elif j > 0 and highest == self.alignmentMatrix[i][j-1]:
				self.traceback.append([i, j-1])
				self.seq1.insert(i, GAP_SYMBOL)
				j -= 1
			else:
				print 'unexpected value at traceback'
				raise SystemExit

			compliants = [minimum, minimum, minimum]

		self.isAligned = True

	def generateCMP(self):
		if not self.isAligned:
			print 'must align first'
			raise SystemExit
		for i in xrange(len(self.seq1)):
			if self.seq1[i] == GAP_SYMBOL or self.seq2[i] == GAP_SYMBOL:
				self.cmp += GAP_SYMBOL
			elif self.seq1[i] == self.seq2[i]:
				self.cmp += MATCH_SYMBOL
			else:
				self.cmp += MISMATCH_SYMBOL

	def compare(self):
		self.generateAlignmentMatrix()
		self.align()
		self.generateCMP()

	def getAlignmentScore(self):
		return self.alignmentMatrix[-1][-1]
