import sys, time

# TODO check if tokens are grabbking K's

black_pieces = {}
red_pieces = {}
black_initial = ''
red_initial = ''
black_name = ''
red_name = ''
board_size = 0
pieces_removed = {}
last_token_removed = ''

def main():
	setup_board()
	play()


def setup_board():
	get_players_initials()
	get_board_size()
	create_starting_pieces()
	display_board()


def get_players_initials():
	global black_name, red_name, black_initial, red_initial
	print('\n\n')
	print('Let\'s get your names.')
	while True:
		black_name = input('What\'s player 1\'s name? ').title()
		red_name = input('What\'s player 2\'s name? ').title()
		black_initial = black_name[0:1]
		red_initial = red_name[0:1]
		if black_initial != red_initial:
			refresh(3)
			break
		else:
			refresh(3)
			print('First initials can\'t match.')


def get_board_size():
	global board_size

	print('What size board do you want to play with?')
	print('Must be an even number between 6 and 12.')
	bad = True
	while bad:
		try:
			board_size = int(input('Your selection: '))
			if board_size % 2 == 0:
				if board_size <= 12 and board_size >= 6:
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
	refresh(3)


def refresh(lines):
	for i in range(lines):
		sys.stdout.write("\033[F") # Cursor up one line
	for i in range(lines):
		print(' '*60)	# clears any previously printed characters up end of terminal line
	for i in range(lines):
		sys.stdout.write("\033[F") # Cursor up one line
	sys.stdout.flush()


def create_starting_pieces():
	for x in range(board_size):
		for y in range(board_size):
			if x < ((board_size - 2) / 2):	# If on black's side of the board
				if x % 2 != 0:
					if y % 2 != 0:
						black_pieces[str([x,y])] = 'N'
				else:
					if y % 2 == 0:
						black_pieces[str([x,y])] = 'N'
			elif x > (((board_size - 2) / 2) + 1):	# If on red's side of the board
				if x % 2 != 0:
					if y % 2 != 0:
						red_pieces[str([x,y])] = 'N'
				else:
					if y % 2 == 0:
						red_pieces[str([x,y])] = 'N'


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
			if str([x,y]) in black_pieces:
				if black_pieces.get(str([x,y])) == 'N':
					row = row + ' ' + black_initial + ' |'
				elif black_pieces.get(str([x,y])) == 'K':
					row = row + '<' + black_initial + '>|'
			elif str([x,y]) in red_pieces:
				if red_pieces.get(str([x,y])) == 'N':
					row = row + ' ' + red_initial + ' |'
				elif red_pieces.get(str([x,y])) == 'K':
					row = row + '<' + red_initial + '>|'
			elif (x % 2 == 0 and y % 2 != 0) or (x % 2 != 0 and y % 2 == 0):
				row = row + ' * |'
			elif str([x,y]) in pieces_removed:
				if pieces_removed.get(str([x,y])) == 'N':
					row = row + '>' + last_token_removed + '<|'
				elif pieces_removed.get(str([x,y])) == 'K':
					row = row + '{' + last_token_removed + '}|'
			else:
				row = row + '   |'
		if x < 9:
			row = row + '  ' + str(x + 1)
		else:
			row = row + ' ' + str(x + 1)
		playable_rows.append(row)

	return playable_rows


def convert_to_list(string):
	back_to_list = list(string)

	checklist = ['[',']',',',' ']
	for character in checklist:
		while character in back_to_list:
			back_to_list.remove(character)

	return back_to_list


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
			print('Round {0}, {1}\'s turn'.format(turn, black_name))
			turn, jumped, move_selection = player_turn(black_pieces, red_pieces, turn, jumped, move_selection, 'O')
		else:
			print('Round {0}, {1}\'s turn'.format(turn, red_name))
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
		print('You must move this piece.')
		piece_selection = moved_piece
	else:
		piece_selection = select_piece(player_pieces, opponent_pieces)
	move_selection, piece_type, jumped_piece, jumped_piece_type = select_move(piece_selection, player_pieces, opponent_pieces)

	jumped = False
	if last_token_removed != token:
		pieces_removed.clear()

	if jumped_piece != None:
		opponent_pieces.pop(str([int(jumped_piece[0]),int(jumped_piece[1])]))
		pieces_removed[str([int(jumped_piece[0]),int(jumped_piece[1])])] = jumped_piece_type
		last_token_removed = token
		if can_jump(move_selection, player_pieces, opponent_pieces):
			turn = turn - 1
			jumped = True
	player_pieces.pop(str(piece_selection))
	player_pieces[str(move_selection)] = piece_type
	king_me(move_selection, player_pieces)
	refresh_rate = 36 - ((12-board_size)*2)
	refresh((36-((12-board_size)*2)))
	display_board()

	return turn, jumped, move_selection


def select_piece(player_pieces,opponent_pieces):
	invalid = True
	print('\nPlease select which piece you would like to move.')
	while invalid:
		refresh_rate = 2
		try:
			y = int(input('Choose a number on the x (vertical) axis: ')) - 1
			refresh_rate = 3
			x = int(input('Choose a number on the y (horizontal) axis: ')) - 1
			if str([x,y]) in player_pieces and (can_move(x,y,player_pieces,opponent_pieces) or can_jump([x,y],player_pieces,opponent_pieces)):
				invalid = False
				return [x,y]
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
			y = int(input('Choose a number on the x (vertical) axis: ')) - 1
			refresh_rate = 3
			x = int(input('Choose a number on the y (horizontal) axis: ')) - 1
			jumped_piece = [((x + piece[0]) / 2),((y + piece[1]) / 2)]
			if empty(x,y,player_pieces,opponent_pieces) and one_space_away(x,y,piece):
				invalid = False
				return [x,y], 'N', None, None
			elif empty(x,y,player_pieces,opponent_pieces) and two_spaces_away(x,y,piece) and jumping(jumped_piece,opponent_pieces):
					jumped_piece_type = opponent_pieces.get(str([int(jumped_piece[0]),int(jumped_piece[1])]))
					invalid = False
					return [x,y], 'N', jumped_piece, jumped_piece_type
			else:
				refresh(3)
				print('Invalid selection. Please select a different square.')
		except ValueError:
			refresh(refresh_rate)
			print('Input must be an integer. Please try again.')


def empty(x,y,player_pieces,opponent_pieces):
	if str([x,y]) not in player_pieces and str([x,y]) not in opponent_pieces:
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
	if jumped_piece[0] % 1 == 0 and jumped_piece[1] % 1 == 0:
		if str([int(jumped_piece[0]),int(jumped_piece[1])]) in opponent_pieces:
			return True
		else:
			return False
	else:
		return False


def can_jump(selection, player_pieces, opponent_pieces):
	possible = False
	if str([selection[0] - 1, selection[1] - 1]) in opponent_pieces and str([selection[0] - 2, selection[1] - 2]) not in player_pieces and str([selection[0] - 2, selection[1] - 2]) not in opponent_pieces:
		if x-2 >= 0 and y-2 >= 0:
			possible = True
	if str([selection[0] + 1, selection[1] - 1]) in opponent_pieces and str([selection[0] + 2, selection[1] - 2]) not in player_pieces and str([selection[0] + 2, selection[1] - 2]) not in opponent_pieces:
		if x+2 <= (board_size - 1) and y-2 >= 0:
			possible = True
	if str([selection[0] - 1, selection[1] + 1]) in opponent_pieces and str([selection[0] - 2, selection[1] + 2]) not in player_pieces and str([selection[0] - 2, selection[1] + 2]) not in opponent_pieces:
		if x-2 >= 0 and y+2 <= (board_size - 1):
			possible = True
	if str([selection[0] + 1, selection[1] + 1]) in opponent_pieces and str([selection[0] + 2, selection[1] + 2]) not in player_pieces and str([selection[0] + 2, selection[1] + 2]) not in opponent_pieces:
		if x+2 <= (board_size - 1) and y+2 <= (board_size - 1):
			possible = True

	return possible


def can_move(x, y, player_pieces, opponent_pieces):
	possible = False
	if str([x - 1, y - 1]) not in player_pieces and str([x - 1, y - 1]) not in opponent_pieces:
		if x-1 >= 0 and y-1 >= 0:
			possible = True
	if str([x + 1, y - 1]) not in player_pieces and str([x + 1, y - 1]) not in opponent_pieces:
		if x+1 <= (board_size - 1) and y-1 >= 0:
			possible = True
	if str([x - 1, y + 1]) not in player_pieces and str([x - 1, y + 1]) not in opponent_pieces:
		if x-1 >= 0 and y+1 <= (board_size - 1):
			possible = True
	if str([x + 1, y + 1]) not in player_pieces and str([x + 1, y + 1]) not in opponent_pieces:
		if x+1 <= (board_size - 1) and y+1 <= (board_size - 1):
			possible = True

	return possible


def king_me(move_selection, player_pieces):
	if move_selection[0] == 0 or move_selection[0] == board_size - 1:
		player_pieces.pop(str(move_selection))
		player_pieces[str(move_selection)]='K'


if __name__ == '__main__':
	main()
