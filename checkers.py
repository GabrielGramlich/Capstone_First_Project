import sys, time

black_pieces = []
red_pieces = []
board_size = 0

def main():
	setup_board()


def setup_board():
	get_board_size()
	create_starting_pieces()
	display_board()
	play()


def get_board_size():
	global board_size

	print('What size board do you want to play with?')
	print('Must be an even number between 6 and 12.')
	board_size = valid_size()
	refresh(3)


def valid_size():
	bad = True
	while bad:
		try:
			size = int(input('Your selection: '))
			if size % 2 == 0:
				if size <= 12 and size >= 6:
					bad = False
				else:
					refresh(2)
					print('Input must be between 6 and 12.')
			else:
				refresh(2)
				print('Input must be an even number.')
		except ValueError:
			refresh(2)
			print('Input must be an integer.')

	return size


def refresh(lines):
	for i in range(lines):
		sys.stdout.write("\033[F") # Cursor up one line
	for i in range(lines):
		print(' '*55)	# clears any previously printed characters up end of terminal line
	for i in range(lines):
		sys.stdout.write("\033[F") # Cursor up one line
	sys.stdout.flush()


def create_starting_pieces():
	for x in range(board_size):
		for y in range(board_size):
			if x < ((board_size - 2) / 2):	# If on black's side of the board
				if x % 2 != 0:
					if y % 2 != 0:
						black_pieces.append([x,y])
				else:
					if y % 2 == 0:
						black_pieces.append([x,y])
			elif x > (((board_size - 2) / 2) + 1):	# If on red's side of the board
				if x % 2 != 0:
					if y % 2 != 0:
						red_pieces.append([x,y])
				else:
					if y % 2 == 0:
						red_pieces.append([x,y])


def display_board():
	cap_row, filler_row = get_nonplayable_rows()
	playable_rows = get_playable_rows()
	propogate_pieces(cap_row, filler_row, playable_rows)


def get_nonplayable_rows():
	cap_row = '  '
	for i in range(board_size):
		if i < 10:
			cap_row = cap_row + '   ' + str(i + 1)
		else:
			cap_row = cap_row + '  ' + str(i + 1)
	filler_row = '   ' + ('*---' * board_size) + '*'

	return cap_row, filler_row


def get_playable_rows():
	playable_rows = []
	for x in range(board_size):
		if x < 9:
			row = str(x + 1) + '  |'
		else:
			row = str(x + 1) + ' |'
		for y in range(board_size):
			if [x,y] in black_pieces:
				row = row + ' X |'
			elif [x,y] in red_pieces:
				row = row + ' O |'
			else:
				row = row + '   |'
		if x < 9:
			row = row + '  ' + str(x + 1)
		else:
			row = row + ' ' + str(x + 1)
		playable_rows.append(row)

	return playable_rows


def propogate_pieces(cap_row, filler_row, playable_rows):
	print(cap_row)
	print(filler_row)
	for i in range(len(playable_rows)):
		print(playable_rows[i])
		print(filler_row)
	print(cap_row)


def play():
	turn = 0
	while True:
		turn = turn + 1
		if turn % 2 == 0:
			print('Round {}, player O goes'.format(turn))
			turn = player_turn(red_pieces, black_pieces, turn)
		else:
			print('Round {}, player X goes'.format(turn))
			turn = player_turn(black_pieces, red_pieces, turn)
		# TODO make move
		# TODO continue if allowed
		# TODO switch player


def player_turn(player_pieces, opponent_pieces, turn):
	piece_selection = select_piece(player_pieces)
	move_selection, jumped_piece = select_move(piece_selection, player_pieces, opponent_pieces)
	if jumped_piece != None:
		opponent_pieces.remove(jumped_piece)
		# TODO Validate this
		turn = turn - 1
	player_pieces.remove(piece_selection)
	player_pieces.append(move_selection)
	player_pieces.sort()
	refresh_rate = 36 - ((12-board_size)*2)
	refresh((36-((12-board_size)*2)))
	display_board()

	return turn


def select_piece(player_pieces):
	print('\nPlease select which piece you would like to move.')
	y = int(input('Choose a number on the x axis: ')) - 1
	x = int(input('Choose a number on the y axis: ')) - 1
	if [x,y] in player_pieces:
		return [x,y]


def select_move(piece, player_pieces, opponent_pieces):
	invalid = True
	# TODO Validate this
	while invalid:
		print('\nPlease select where you would like to move the piece.')
		y = int(input('Choose a number on the x axis: ')) - 1
		x = int(input('Choose a number on the y axis: ')) - 1
		if [x,y] not in player_pieces and [x,y] not in opponent_pieces:
			if (x - 1 == piece[0] or x + 1 == piece[0]) and (y - 1 == piece[1] or y + 1 == piece[1]):
				invalid = False
				return [x,y], None
			elif (x - 2 == piece[0] or x + 2 == piece[0]) and (y - 2 == piece[1] or y + 2 == piece[1]):
				jumped_piece = [((x + piece[0]) / 2),((y + piece[1]) / 2)]
				if jumped_piece in opponent_pieces:
					invalid = False
					return [x,y], jumped_piece


if __name__ == '__main__':
	main()
