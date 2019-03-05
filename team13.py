from time import time
import copy 
class BigBoard:

	def __init__(self):
		# big_boards_status is the game board
		# small_boards_status shows which small_boards have been won/drawn and by which player
		self.big_boards_status = ([['-' for i in range(9)] for j in range(9)], [['-' for i in range(9)] for j in range(9)])
		self.small_boards_status = ([['-' for i in range(3)] for j in range(3)], [['-' for i in range(3)] for j in range(3)])

	def print_board(self):
		# for printing the state of the board
		print '================BigBoard State================'
		for i in range(9):
			if i%3 == 0:
				print
			for k in range(2):
				for j in range(9):
					if j%3 == 0:
						print "",
					print self.big_boards_status[k][i][j],
				if k==0:
					print "   ",
			print
		print

		print '==============SmallBoards States=============='
		for i in range(3):
			for k in range(2):
				for j in range(3):
					print self.small_boards_status[k][i][j],
				if k==0:
					print "  ",
			print
		print '=============================================='
		print
		print


	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_small_board = [old_move[1]%3, old_move[2]%3]
		#checks if the move is a free move or not based on the rules

		if old_move == (-1,-1,-1) or (self.small_boards_status[0][allowed_small_board[0]][allowed_small_board[1]] != '-' and self.small_boards_status[1][allowed_small_board[0]][allowed_small_board[1]] != '-'):
			for k in range(2):
				for i in range(9):
					for j in range(9):
						if self.big_boards_status[k][i][j] == '-' and self.small_boards_status[k][i/3][j/3] == '-':
							allowed_cells.append((k,i,j))

		else:
			for k in range(2):
				if self.small_boards_status[k][allowed_small_board[0]][allowed_small_board[1]] == "-":
					for i in range(3*allowed_small_board[0], 3*allowed_small_board[0]+3):
						for j in range(3*allowed_small_board[1], 3*allowed_small_board[1]+3):
							if self.big_boards_status[k][i][j] == '-':
								allowed_cells.append((k,i,j))

		return allowed_cells	

	def find_terminal_state(self):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher small_boards in case of a draw

		cntx = 0
		cnto = 0
		cntd = 0
	
		for k in range(2):
			bs = self.small_boards_status[k]
			for i in range(3):
				for j in range(3):
					if bs[i][j] == 'x':
						cntx += 1
					if bs[i][j] == 'o':
						cnto += 1
					if bs[i][j] == 'd':
						cntd += 1
			for i in range(3):
				row = bs[i]
				col = [x[i] for x in bs]
				#print row,col
				#checking if i'th row or i'th column has been won or not
				if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 3):	
					return (row[0],'WON')
				if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 3):
					return (col[0],'WON')
			#check diagonals
			if(bs[0][0] == bs[1][1] == bs[2][2]) and (bs[0][0] == 'x' or bs[0][0] == 'o'):
				return (bs[0][0],'WON')
			if(bs[0][2] == bs[1][1] == bs[2][0]) and (bs[0][2] == 'x' or bs[0][2] == 'o'):
				return (bs[0][2],'WON')

		if cntx+cnto+cntd < 18:		#if all small_boards have not yet been won, continue
			return ('CONTINUE', '-')
		elif cntx+cnto+cntd == 18:							#if game is drawn
			return ('NONE', 'DRAW')

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 3) or (len(new_move) != 3):
			return False
		for i in range(3):
			if (type(old_move[i]) is not int) or (type(new_move[i]) is not int):
				return False
		if (old_move != (-1,-1,-1)) and (old_move[0] < 0 or old_move[0] > 1 or old_move[1] < 0 or old_move[1] > 8 or old_move[2] < 0 or old_move[2] > 8):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells

	def update(self, old_move, new_move, ply):
		#updating the game board and small_board status as per the move that has been passed in the arguements
		if(self.check_valid_move(old_move, new_move)) == False:
			return 0, False
		self.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply

		x = new_move[1]/3
		y = new_move[2]/3
		k = new_move[0]
		fl = 0

		#checking if a small_board has been won or drawn or not after the current move
		bs = self.big_boards_status[k]
		for i in range(3):
			#checking for horizontal pattern(i'th row)
			if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ply):
				self.small_boards_status[k][x][y] = ply
				return 1, True
			#checking for vertical pattern(i'th column)
			if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ply):
				self.small_boards_status[k][x][y] = ply
				return 1, True
		#checking for diagonal patterns
		#diagonal 1
		if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ply):
			self.small_boards_status[k][x][y] = ply
			return 1, True
		#diagonal 2
		if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ply):
			self.small_boards_status[k][x][y] = ply
			return 1, True
		#checking if a small_board has any more cells left or has it been drawn
		for i in range(3):
			for j in range(3):
				if bs[3*x+i][3*y+j] =='-':
					return 1, False
		self.small_boards_status[k][x][y] = 'd'
		return 1, False


class Team13:
	def __init__(self):
		self.chutad = BigBoard()
		self.prev = (-1, -1, -1)
		self.bonus_availed = False
		self.first_move = True
	def pattern_small(self, h, st_i, st_j, in_i, in_j ):
		temp = 0
		f = True

		ti = st_i
		tj = st_j
		for k in range(3):
			if not( self.chutad.big_boards_status[h][ti][tj] == '-' or self.chutad.big_boards_status[h][ti][tj] == 'x' ):
				f = False
				break
			ti += in_i
			tj += in_j
		if f:
			c = 0
			ti = st_i
			tj = st_j
			for k in range(3):
				if self.chutad.big_boards_status[h][ti][tj] == 'x':
					c += 1
				ti += in_i
				tj += in_j
			if c == 3:
				temp += 200
			else:
				temp += c*c
		f = True
		ti = st_i
		tj = st_j
		for k in range(3):
			if not( self.chutad.big_boards_status[h][ti][tj] == '-' or self.chutad.big_boards_status[h][ti][tj] == 'o' ):
				f = False
				break
			ti += in_i
			tj += in_j
		if f:
			c = 0
			ti = st_i
			tj = st_j
			for k in range(3):
				if self.chutad.big_boards_status[h][ti][tj] == 'o':
					c += 1
				ti += in_i
				tj += in_j
			if c == 3:
				temp -= 200
			else:
				temp -= c*c
		return temp
	def pattern_big(self, h, st_i, st_j, in_i, in_j ):
		temp = 0
		f = True

		ti = st_i
		tj = st_j
		for k in range(3):
			if not( self.chutad.small_boards_status[h][ti][tj] == '-' or self.chutad.small_boards_status[h][ti][tj] == 'x' ):
				f = False
				break
			ti += in_i
			tj += in_j
		if f:
			c = 0
			num200s = 0
			ti = st_i
			tj = st_j
			for k in range(3):
				if self.chutad.small_boards_status[h][ti][tj] == 'x':
					c += self.heuristic_small[h][ti][tj]
					if self.heuristic_small[h][ti][tj] == 200:
						num200s += 1
				ti += in_i
				tj += in_j
			if num200s == 3:
				temp += 2000000000
			else:
				temp += c*c
		f = True
		ti = st_i
		tj = st_j
		for k in range(3):
			if not( self.chutad.small_boards_status[h][ti][tj] == '-' or self.chutad.small_boards_status[h][ti][tj] == 'o' ):
				f = False
				break
			ti += in_i
			tj += in_j
		if f:
			c = 0
			num200s = 0
			ti = st_i
			tj = st_j
			for k in range(3):
				if self.chutad.small_boards_status[h][ti][tj] == 'o':
					c += self.heuristic_small[h][ti][tj]
					if self.heuristic_small[h][ti][tj] == 200:
						num200s += 1
				ti += in_i
				tj += in_j
			if num200s == 3:
				temp -= 2000000000
			else:
				temp += c*c
			temp -= c*c
		return temp
	def heuristic( self ):
		# operate on self.chutad

		# number of non blocked patterns
		self.heuristic_small = ( [[0 for j in range(3)] for i in range(3)], [[0 for j in range(3)] for i in range(3)] )
		for h in range(2):
			for i in range(3):
				for j in range(3):
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+0, 3*j+0, 0, 1) # 0,k
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+1, 3*j+0, 0, 1) # 1,k
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+2, 3*j+0, 0, 1) # 2,k
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+0, 3*j+0, 1, 0) # k,0
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+0, 3*j+1, 1, 0) # k,1
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+0, 3*j+2, 1, 0) # k,2
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+0, 3*j+0, 1, 1) # k,k
					self.heuristic_small[h][i][j] += self.pattern_small(h, 3*i+0, 3*j+2, 1, -1) # k,2-k
		temp = [0,0]
		for h in range(2):
			temp[h] += self.pattern_big(h, 0, 0, 0, 1) # 0,k
			temp[h] += self.pattern_big(h, 1, 0, 0, 1) # 1,k
			temp[h] += self.pattern_big(h, 2, 0, 0, 1) # 2,k
			temp[h] += self.pattern_big(h, 0, 0, 1, 0) # k,0
			temp[h] += self.pattern_big(h, 0, 1, 1, 0) # k,1
			temp[h] += self.pattern_big(h, 0, 2, 1, 0) # k,2
			temp[h] += self.pattern_big(h, 0, 0, 1, 1) # k,k
			temp[h] += self.pattern_big(h, 0, 2, 1, -1) # k,2-k

		return temp[0]+temp[1]

	def minimax( self, old_move, flag, depth, alpha, beta ):
		if depth == 0:
			# print " applied heuristic "
			# print " got value ", self.heuristic()
			# print " double tap ", self.heuristic()
			return (-1, self.heuristic())
		# print " CURRENT STATE IS "
		# self.chutad.print_board()
		if flag == 'x':
			f_index = -1
			value = -1000000000000000000
			i = 0
			moves = self.chutad.find_valid_move_cells(old_move)
			if len(moves) > 70:
				moves = moves[0:35] + moves[len(moves)-35:len(moves)]
			for m in moves:
				# print " applying move %d %d %d" %(m[0], m[1], m[2])
				# apply m
				update_status, small_board_won = self.chutad.update(old_move, m, 'x')

				if small_board_won :
					if self.bonus_availed :
						fm_index, fm_value = self.minimax(m, 'o', depth-1, alpha, beta )
					else:
						self.bonus_availed = True
						fm_index, fm_value = self.minimax(m, 'x', depth-1, alpha, beta )
						self.bonus_availed = False
				else:
					fm_index, fm_value = self.minimax(m, 'o', depth-1, alpha, beta )

				# compare with current max
				if( fm_value > value ):
					f_index = i
					value = fm_value
				alpha = max(alpha, value)

				# print " undoing move %d %d %d" %(m[0], m[1], m[2])
				# undo m
				self.chutad.big_boards_status[m[0]][m[1]][m[2]] = '-'
				self.chutad.small_boards_status[m[0]][m[1]/3][m[2]/3] = '-'

				# prune
				if( alpha >= beta ):
					break


				i += 1

		if flag == 'o':
			f_index = -1
			value = +1000000000000000000
			i = 0

			moves = self.chutad.find_valid_move_cells(old_move)
			if len(moves) > 70:
				moves = moves[0:35] + moves[len(moves)-35:len(moves)]
			for m in moves:
				# print " applying move %d %d %d" %(m[0], m[1], m[2])
				# apply m
				update_status, small_board_won = self.chutad.update(old_move, m, 'o')

				if small_board_won :
					if self.bonus_availed :
						fm_index, fm_value = self.minimax(m, 'x', depth-1, alpha, beta )
					else:
						self.bonus_availed = True
						fm_index, fm_value = self.minimax(m, 'o', depth-1, alpha, beta )
						self.bonus_availed = False
				else:
					fm_index, fm_value = self.minimax(m, 'x', depth-1, alpha, beta )

				# compare with current min
				if( fm_value < value ):
					f_index = i
					value = fm_value
				beta = min(beta, value)

				# print " undoing move %d %d %d" %(m[0], m[1], m[2])
				# undo m
				self.chutad.big_boards_status[m[0]][m[1]][m[2]] = '-'
				self.chutad.small_boards_status[m[0]][m[1]/3][m[2]/3] = '-'

				# prune
				if( alpha >= beta ):
					break

				i += 1
		# if f_index == -1:
			# print "NALLA2"
			# self.chutad.print_board()
		return (f_index, value)

	def move(self, board, old_move, flag):
		start = time()
		self.chutad.big_boards_status = copy.deepcopy( board.big_boards_status ) 
		self.chutad.small_boards_status = copy.deepcopy( board.small_boards_status )
		self.prev = old_move
		
		f_index, value = self.minimax( old_move, flag, 5, -1000000000000000000, +1000000000000000000 )
		print time()-start
		print value
		return board.find_valid_move_cells(old_move)[f_index]