import sys, time

black_pieces = []
red_pieces = []
board_size = 0
pieces_removed = []
last_token_removed = ''

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
						black_pieces.append([x,y,'N'])
				else:
					if y % 2 == 0:
						black_pieces.append([x,y,'N'])
			elif x > (((board_size - 2) / 2) + 1):	# If on red's side of the board
				if x % 2 != 0:
					if y % 2 != 0:
						red_pieces.append([x,y,'N'])
				else:
					if y % 2 == 0:
						red_pieces.append([x,y,'N'])


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
			if [x,y,'N'] in black_pieces:
				row = row + ' X |'
			elif [x,y,'N'] in red_pieces:
				row = row + ' O |'
			elif (x % 2 == 0 and y % 2 != 0) or (x % 2 != 0 and y % 2 == 0):
				row = row + ' * |'
			elif [x,y,'N'] in pieces_removed:
				row = row + '{' + last_token_removed + '}|'
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
	jumped = False
	move_selection = []
	while True:
		turn = turn + 1
		if turn % 2 != 0:
			print('Round {}, player X goes'.format(turn))
			turn, jumped, move_selection = player_turn(black_pieces, red_pieces, turn, jumped, move_selection, 'O')
		else:
			print('Round {}, player O goes'.format(turn))
			turn, jumped, move_selection = player_turn(red_pieces, black_pieces, turn, jumped, move_selection, 'X')
		if len(black_pieces) == 0:
			print('X\'s win!')
			break
		elif len(red_pieces) == 0:
			print('O\'s win!')
			break


def player_turn(player_pieces, opponent_pieces, turn, jumped, moved_piece, token):
	global pieces_removed, last_token_removed

	if jumped:
		print('\nLast piece moved:')
		print(str(moved_piece[1] + 1) + ',' + str(moved_piece[0] + 1))
		piece_selection = moved_piece
	else:
		piece_selection = select_piece(player_pieces, opponent_pieces)
	move_selection, jumped_piece = select_move(piece_selection, player_pieces, opponent_pieces)

	jumped = False
	if last_token_removed != token:
		pieces_removed.clear()

	if jumped_piece != None:
		opponent_pieces.remove(jumped_piece)
		pieces_removed.append(jumped_piece)
		last_token_removed = token
		if can_jump(move_selection, player_pieces, opponent_pieces):
			turn = turn - 1
			jumped = True
	player_pieces.remove(piece_selection)
	player_pieces.append(move_selection)
	player_pieces.sort()
	refresh_rate = 36 - ((12-board_size)*2)
	refresh((36-((12-board_size)*2)))
	display_board()

	return turn, jumped, move_selection


def select_piece(player_pieces,opponent_pieces):
	# TODO Validate that this piece can move
	invalid = True
	print('\nPlease select which piece you would like to move.')
	while invalid:
		refresh_rate = 2
		try:
			y = int(input('Choose a number on the x axis: ')) - 1
			refresh_rate = 3
			x = int(input('Choose a number on the y axis: ')) - 1
			if [x,y,'N'] in player_pieces and can_move(x,y,player_pieces,opponent_pieces):
				invalid = False
				return [x,y,'N']
			else:
				refresh(3)
				print('Invalid selection. Please select a different piece.')
		except ValueError:
			refresh(refresh_rate)
			print('Input must be an integer. Please try again.')



def select_move(piece, player_pieces, opponent_pieces):
	# TODO Keep player from moving backwards if not kinged
	# TODO King players at end of board
	invalid = True
	print('\nPlease select where you would like to move the piece.')
	while invalid:
		refresh_rate = 2
		try:
			y = int(input('Choose a number on the x axis: ')) - 1
			refresh_rate = 3
			x = int(input('Choose a number on the y axis: ')) - 1
			jumped_piece = [((x + piece[0]) / 2),((y + piece[1]) / 2),'N']
			if empty(x,y,player_pieces,opponent_pieces) and one_space_away(x,y,piece):
				invalid = False
				return [x,y,'N'], None
			elif empty(x,y,player_pieces,opponent_pieces) and two_spaces_away(x,y,piece) and jumping(jumped_piece,opponent_pieces):
					invalid = False
					return [x,y,'N'], jumped_piece
			else:
				refresh(3)
				print('Invalid selection. Please select a different square.')
		except ValueError:
			refresh(refresh_rate)
			print('Input must be an integer. Please try again.')


def empty(x,y,player_pieces,opponent_pieces):
	if [x,y,'N'] not in player_pieces and [x,y,'N'] not in opponent_pieces:
		return True
	else:
		return False


def one_space_away(x,y,piece):
	if (x - 1 == piece[0] or x + 1 == piece[0]) and (y - 1 == piece[1] or y + 1 == piece[1]):
		return True
	else:
		return False


def two_spaces_away(x,y,piece):
	if (x - 2 == piece[0] or x + 2 == piece[0]) and (y - 2 == piece[1] or y + 2 == piece[1]):
		return True
	else:
		return False


def jumping(jumped_piece,opponent_pieces):
	if jumped_piece in opponent_pieces:
		return True
	else:
		return False


def can_jump(selection, player_pieces, opponent_pieces):
	possible = False
	if [selection[0] - 1, selection[1] - 1] in opponent_pieces and [selection[0] - 2, selection[1] - 2] not in player_pieces and [selection[0] - 2, selection[1] - 2] not in opponent_pieces:
		possible = True
	if [selection[0] + 1, selection[1] - 1] in opponent_pieces and [selection[0] + 2, selection[1] - 2] not in player_pieces and [selection[0] + 2, selection[1] - 2] not in opponent_pieces:
		possible = True
	if [selection[0] - 1, selection[1] + 1] in opponent_pieces and [selection[0] - 2, selection[1] + 2] not in player_pieces and [selection[0] - 2, selection[1] + 2] not in opponent_pieces:
		possible = True
	if [selection[0] + 1, selection[1] + 1] in opponent_pieces and [selection[0] + 2, selection[1] + 2] not in player_pieces and [selection[0] + 2, selection[1] + 2] not in opponent_pieces:
		possible = True

	return possible


def can_move(x, y, player_pieces, opponent_pieces):
	possible = False
	if [x - 1, y - 1, 'N'] not in player_pieces and [x - 1, y - 1, 'N'] not in opponent_pieces:
		possible = True
	if [x + 1, y - 1, 'N'] not in player_pieces and [x + 1, y - 1, 'N'] not in opponent_pieces:
		possible = True
	if [x - 1, y + 1, 'N'] not in player_pieces and [x - 1, y + 1, 'N'] not in opponent_pieces:
		possible = True
	if [x + 1, y + 1, 'N'] not in player_pieces and [x + 1, y + 1, 'N'] not in opponent_pieces:
		possible = True

	return possible


if __name__ == '__main__':
	main()
