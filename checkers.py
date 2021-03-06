import sys, time

# TODO make validation messages more meaningful
# TODO add comments
# TODO make code follow SRP
# TODO organize code by section
# TODO show piece selected

black_pieces = {}
red_pieces = {}
black_initial = ''
red_initial = ''
black_name = ''
red_name = ''
board_size = 0
pieces_removed = {}
last_token_removed = ''
last_piece_moved = []
black_count = 0
red_count = 0


def main():
	setup_board()
	play()


def setup_board():
	get_players_info()
	get_board_size()
	create_starting_pieces()
	get_piece_counts()
	display_board(1, black_initial)


def get_players_info():
	print('\n\n\nLet\'s get your names.')
	while True:
		get_player_names()
		get_players_initials()
		refresh(3)
		if valid_initials():
			break
		else:
			print('First initials can\'t match.')


def get_player_names():
	global black_name, red_name

	black_name = input('What\'s player 1\'s name? ').title()
	red_name = input('What\'s player 2\'s name? ').title()


def get_players_initials():
	global black_initial, red_initial

	black_initial = black_name[0:1]
	red_initial = red_name[0:1]


def refresh(lines):
	for i in range(lines):
		sys.stdout.write("\033[F") # Cursor up one line
	for i in range(lines):
		print(' '*60)	# clears any previously printed characters up end of terminal line
	for i in range(lines):
		sys.stdout.write("\033[F") # Cursor up one line
	sys.stdout.flush()


def valid_initials():
	return black_initial != red_initial


def get_board_size():
	print('What size board do you want to play with?')
	print('Must be an even number between 6 and 12.')
	bad = True
	while bad:
		bad = valid_board_size(input('Your selection: '))
	refresh(3)


def valid_board_size(input_size):
	global board_size

	try:
		board_size = int(input_size)

		if not in_range(board_size, 12, 6):
			refresh(2)
			print('Input must be between 6 and 12.')
			return True
		elif not is_even(board_size):
			refresh(2)
			print('Input must be an even number.')
			return True
		else:
			return False
	except ValueError:
		refresh(2)
		print('Input must be an integer.')
		return True


def in_range(test_number, high, low):
	return test_number <= high and test_number >= low


def is_even(test_number):
	return test_number % 2 == 0


def create_starting_pieces():
	for x in range(board_size):
		for y in range(board_size):
			if is_black(x):
				create_piece(x,y,black_pieces)
			elif is_red(x):
				create_piece(x,y,red_pieces)


def is_black(x):
	return x < ((board_size - 2) / 2)


def is_red(x):
	return x > ((board_size - 2) / 2) + 1


def create_piece(x,y,pieces):
	if not is_even(x):
		if not is_even(y):
			pieces[str([x,y])] = 'N'
	else:
		if is_even(y):
			pieces[str([x,y])] = 'N'


def get_piece_counts():
	global black_count, red_count

	black_count = len(black_pieces)
	red_count = len(red_pieces)


def display_board(turn, token):
	cap_row, filler_row = get_nonplayable_rows()
	playable_rows = get_playable_rows()
	info_row, black_row, red_row, current_player_row = get_display_rows(turn, token)
	propogate_pieces(cap_row, filler_row, playable_rows, info_row, black_row, red_row, current_player_row)


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
		row = start_row(x)
		for y in range(board_size):
			row = row + continue_row(str([x,y]),x,y)
		row = row + finish_row(x)
		playable_rows.append(row)

	return playable_rows


def start_row(x):
	if x < 9:
		return str(x + 1) + '  |'
	else:
		return str(x + 1) + ' |'


def continue_row(piece,x,y):
	if piece == str(last_piece_moved):
		return get_moved_piece_section(piece)
	elif piece in black_pieces:
		return get_normal_piece_section(piece,black_pieces,black_initial)
	elif piece in red_pieces:
		return get_normal_piece_section(piece,red_pieces,red_initial)
	elif is_off_square(x,y):
		return ' * |'
	elif piece in pieces_removed:
		return get_removed_piece_section(piece)
	else:
		return '   |'


def get_moved_piece_section(piece):
	if piece in black_pieces:
		return '|' + black_initial + '||'
	elif piece in red_pieces:
		return '|' + red_initial + '||'


def get_normal_piece_section(piece,pieces,initial):
	if pieces.get(piece) == 'N':
		return ' ' + initial + ' |'
	elif pieces.get(piece) == 'K':
		return '<' + initial + '>|'


def is_off_square(x,y):
	return (x % 2 == 0 and y % 2 != 0) or (x % 2 != 0 and y % 2 == 0)


def get_removed_piece_section(piece):
	if pieces_removed.get(piece) == 'N':
		return '>' + last_token_removed + '<|'
	elif pieces_removed.get(piece) == 'K':
		return '{' + last_token_removed + '}|'


def finish_row(x):
	if x < 9:
		return '  ' + str(x + 1)
	else:
		return ' ' + str(x + 1)


def get_display_rows(turn, token):
	pad_count = get_pad_count()
	info_row = 'Pieces remaining:'
	black_row = get_player_row(black_name,pad_count,black_count)
	red_row = get_player_row(red_name,pad_count,red_count)
	if token == black_initial:
		current_player_row = 'Round {0}: {1}'.format(turn, black_name)
	elif token == red_initial:
		current_player_row = 'Round {0}: {1}'.format(turn, red_name)

	return info_row, black_row, red_row, current_player_row


def get_pad_count():
	pad_count = 15
	if len(black_name) >= len(red_name):
		if len(black_name) > pad_count:
			pad_count = len(black_name) + 3
	else:
		if len(red_name) > pad_count:
			pad_count = len(red_name) + 3

	return pad_count


def get_player_row(player_name,pad_count,player_count):
	return '{0}{1}'.format(pad_string(player_name + ':', pad_count, False), player_count)


def pad_string(string, pad_count, is_left=True, character=' '):
	while len(string) < pad_count:
		if is_left:
			string = character + string
		else:
			string = string + character
	return string


def propogate_pieces(cap_row, filler_row, playable_rows, info_row, black_row, red_row, current_player_row):
	print(cap_row)
	print(filler_row)
	for i in range(len(playable_rows)):
		print(playable_rows[i])
		print(filler_row)
	print(cap_row)
	print()
	print(info_row)
	print(black_row)
	print(red_row)
	print(current_player_row)


def play():
	turn = 0
	jumping = False
	move_selection = []
	while True:
		turn = turn + 1
		turn, jumping, move_selection = start_turn(turn, jumping, move_selection)
		break_loop = end_game(turn)
		if break_loop:
			break


def start_turn(turn, jumping, move_selection):
	if turn % 2 != 0:
		turn, jumping, move_selection = player_turn(black_pieces, red_pieces, turn, jumping, move_selection, black_initial, red_initial)
	else:
		turn, jumping, move_selection = player_turn(red_pieces, black_pieces, turn, jumping, move_selection, red_initial, black_initial)

	return turn, jumping, move_selection


def player_turn(player_pieces, opponent_pieces, turn, jumping, moved_piece, token, opponent_token):
	piece_selection = get_piece(jumping, moved_piece, player_pieces, opponent_pieces, token)
	refresh_rate = set_refresh_rate(36):
	refresh(refresh_rate)
	display_board(turn, token)
	move_selection, piece_type, jumped_piece, jumped_piece_type = select_valid_move(piece_selection, player_pieces, opponent_pieces, token)
	jumping, turn = update_pieces(player_pieces, opponent_pieces, turn, token, opponent_token, piece_selection, move_selection, piece_type, jumped_piece, jumped_piece_type)
	refresh(refresh_rate)
	display_board(turn, opponent_token)

	return turn, jumping, move_selection


def set_refresh_rate(rate):
	return rate - ((12-board_size)*2)


def get_piece(jumping, moved_piece, player_pieces, opponent_pieces, token):
	if jumping:
		display_jumping_piece(moved_piece)
		return moved_piece
	else:
		return get_non_jumping_piece(player_pieces, opponent_pieces, token)


def display_jumping_piece(moved_piece):
	print('\nLast piece moved:')
	print(str(moved_piece[1] + 1) + ',' + str(moved_piece[0] + 1))
	print('You must move this piece.')


def get_non_jumping_piece(player_pieces, opponent_pieces, token):
	while True:
		piece_selection = select_piece(player_pieces, opponent_pieces, token)
		response = confirm_selection()
		if response == 'y':
			break
		else:
			refresh(4)

	return piece_selection


def select_piece(player_pieces,opponent_pieces,token):
	invalid = True
	print('\nPlease select which piece you would like to move.')
	while invalid:
		refresh_rate = 2
		x,y,refresh_rate = get_selection(refresh_rate)
		selection = [x,y]
		if (str(selection) in player_pieces and (can_move(selection,player_pieces,opponent_pieces, token))) or (str(selection) in player_pieces and can_jump(selection,player_pieces,opponent_pieces,token)):
			invalid = False
			return [x,y]
		else:
			refresh(3)
			print('Invalid selection. Please select a different piece.')



def can_move(selection, player_pieces, opponent_pieces, token):
	piece_type = player_pieces.get(str(selection))

	possible = False
	if piece_type == 'K' or token == red_initial:
		possible = red_can_move(possible, selection, player_pieces, opponent_pieces)
	if piece_type == 'K' or token == black_initial:
		possible = black_can_move(possible, selection, player_pieces, opponent_pieces)

	return possible


def red_can_move(possible, selection, player_pieces, opponent_pieces):
	if str([selection[0] - 1, selection[1] - 1]) not in player_pieces and str([selection[0] - 1, selection[1] - 1]) not in opponent_pieces:
		if selection[0]-1 >= 0 and selection[1]-1 >= 0:
			possible = True
	if str([selection[0] - 1, selection[1] + 1]) not in player_pieces and str([selection[0] - 1, selection[1] + 1]) not in opponent_pieces:
		if selection[0]-1 >= 0 and selection[1]+1 <= (board_size - 1):
			possible = True

	return possible


def black_can_move(possible, selection, player_pieces, opponent_pieces):
	if str([selection[0] + 1, selection[1] - 1]) not in player_pieces and str([selection[0] + 1, selection[1] - 1]) not in opponent_pieces:
		if selection[0]+1 <= (board_size - 1) and selection[1]-1 >= 0:
			possible = True
	if str([selection[0] + 1, selection[1] + 1]) not in player_pieces and str([selection[0] + 1, selection[1] + 1]) not in opponent_pieces:
		if selection[0]+1 <= (board_size - 1) and selection[1]+1 <= (board_size - 1):
			possible = True

	return possible


def can_jump(selection, player_pieces, opponent_pieces, token):
	piece_type = player_pieces.get(str(selection))

	possible = False
	if piece_type == 'K' or token == red_initial:
		possible = red_can_jump(possible, selection, player_pieces, opponent_pieces)
	if piece_type == 'K' or token == black_initial:
		possible = black_can_jump(possible, selection, player_pieces, opponent_pieces)

	return possible


def red_can_jump(possible, selection, player_pieces, opponent_pieces):
	if str([selection[0] - 1, selection[1] - 1]) in opponent_pieces and str([selection[0] - 2, selection[1] - 2]) not in player_pieces and str([selection[0] - 2, selection[1] - 2]) not in opponent_pieces:
		if selection[0]-2 >= 0 and selection[1]-2 >= 0:
			possible = True
	if str([selection[0] - 1, selection[1] + 1]) in opponent_pieces and str([selection[0] - 2, selection[1] + 2]) not in player_pieces and str([selection[0] - 2, selection[1] + 2]) not in opponent_pieces:
		if selection[0]-2 >= 0 and selection[1]+2 <= (board_size - 1):
			possible = True

	return possible


def black_can_jump(possible, selection, player_pieces, opponent_pieces):
	if str([selection[0] + 1, selection[1] - 1]) in opponent_pieces and str([selection[0] + 2, selection[1] - 2]) not in player_pieces and str([selection[0] + 2, selection[1] - 2]) not in opponent_pieces:
		if selection[0]+2 <= (board_size - 1) and selection[1]-2 >= 0:
			possible = True
	if str([selection[0] + 1, selection[1] + 1]) in opponent_pieces and str([selection[0] + 2, selection[1] + 2]) not in player_pieces and str([selection[0] + 2, selection[1] + 2]) not in opponent_pieces:
		if selection[0]+2 <= (board_size - 1) and selection[1]+2 <= (board_size - 1):
			possible = True

	return possible


def confirm_selection():
	response = ''
	while response_invalid(response):
		response = input('Are you satisfied with your selection? (y/n) ').lower()
		if response_invalid(response):
			refresh(1)
	refresh(1)

	return response


def response_invalid(response):
	return response != 'n' and response != 'y'


def select_valid_move(piece_selection, player_pieces, opponent_pieces, token):
	while True:
		move_selection, piece_type, jumped_piece, jumped_piece_type = select_move(piece_selection, player_pieces, opponent_pieces, token)
		response = confirm_selection()
		if response == 'y':
			break
		else:
			refresh(4)

	return move_selection, piece_type, jumped_piece, jumped_piece_type


def select_move(piece, player_pieces, opponent_pieces, token):
	invalid = True
	print('\nPlease select where you would like to move the piece.')
	while invalid:
		refresh_rate = 2
		x,y,refresh_rate = get_selection(refresh_rate)
		jumped_piece = get_jumped_piece(x,y,piece)
		if can_move_one_space(x,y,player_pieces,opponent_pieces,piece,token):
			invalid = False
			return [x,y], player_pieces.get(str(piece)), None, None
		elif can_move_two_spaces(x,y,player_pieces,opponent_pieces,piece,jumped_piece,token):
				jumped_piece_type = opponent_pieces.get(str([int(jumped_piece[0]),int(jumped_piece[1])]))
				invalid = False
				return [x,y], player_pieces.get(str(piece)), jumped_piece, jumped_piece_type
		else:
			refresh(3)
			print('Invalid selection. Please select a different square.')


def get_selection(refresh_rate):
	try:
		y = int(input('Choose a number on the x (vertical) axis: ')) - 1
		refresh_rate = 3
		x = int(input('Choose a number on the y (horizontal) axis: ')) - 1
		return x, y, refresh_rate
	except ValueError:
		refresh(refresh_rate)
		print('Input must be an integer. Please try again.')
		return None, None, refresh_rate


def get_jumped_piece(x,y,piece):
	return [((x + piece[0]) / 2),((y + piece[1]) / 2)]


def can_move_one_space(x,y,player_pieces,opponent_pieces,piece,token):
	return empty(x,y,player_pieces,opponent_pieces) and one_space_away(x,y,piece) and is_moving_forward(piece, [x,y], player_pieces, token)


def can_move_two_spaces(x,y,player_pieces,opponent_pieces,piece,jumped_piece,token):
	return empty(x,y,player_pieces,opponent_pieces) and two_spaces_away(x,y,piece) and jumping(jumped_piece,opponent_pieces) and is_moving_forward(piece, [x,y], player_pieces, token)


def empty(x,y,player_pieces,opponent_pieces):
	if str([x,y]) not in player_pieces and str([x,y]) not in opponent_pieces:
		return True
	else:
		return False


def one_space_away(x,y,piece):
	if ((x - 1 == piece[0] or x + 1 == piece[0]) and (y - 1 == piece[1] or y + 1 == piece[1]) and not off_board([x,y])):
		print(str(x) + "," + str(y))
		print(piece)
		time.sleep(10)
		return True
	else:
		return False


def off_board(selection):
	if selection[1] < 0 or selection [1] >= board_size:
		return True
	elif selection[0] < 0 or selection [0] >= board_size:
		return True
	else:
		return False


def is_moving_forward(old_position, new_position, player_pieces, token):
	piece_type = player_pieces.get(str(old_position))

	moving_forward = False
	if piece_type == 'K':
		moving_forward = True
	elif piece_type == 'N' and token == black_initial:
		if old_position[0] < new_position[0]:
			moving_forward = True
	elif piece_type == 'N' and token == red_initial:
		if old_position[0] > new_position[0]:
			moving_forward = True

	return moving_forward


def two_spaces_away(x,y,piece):
	if ((x - 2 == piece[0] or x + 2 == piece[0]) and (y - 2 == piece[1] or y + 2 == piece[1]) and not off_board([x,y])):
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


def update_pieces(player_pieces, opponent_pieces, turn, token, opponent_token, piece_selection, move_selection, piece_type, jumped_piece, jumped_piece_type):
	jumping = False
	if last_token_removed != opponent_token:
		pieces_removed.clear()

	if jumped_piece != None:
		update_counts(opponent_token)
		update_jumped_pieces(opponent_pieces,jumped_piece,jumped_piece_type,opponent_token)
		if can_jump(move_selection, player_pieces, opponent_pieces, token):
			turn = turn - 1
			jumping = True
	update_piece_ownership(player_pieces,piece_selection,move_selection,piece_type)
	king_me(move_selection, player_pieces)

	return jumping, turn


def update_counts(opponent_token):
	global black_count, red_count

	if opponent_token == black_initial:
		black_count = black_count - 1
	elif opponent_token == red_initial:
		red_count = red_count - 1


def update_jumped_pieces(opponent_pieces,jumped_piece,jumped_piece_type,opponent_token):
	global last_token_removed, pieces_removed

	opponent_pieces.pop(str([int(jumped_piece[0]),int(jumped_piece[1])]))
	pieces_removed[str([int(jumped_piece[0]),int(jumped_piece[1])])] = jumped_piece_type
	last_token_removed = opponent_token


def update_piece_ownership(player_pieces,piece_selection,move_selection,piece_type):
	global last_piece_moved

	player_pieces.pop(str(piece_selection))
	player_pieces[str(move_selection)] = piece_type
	last_piece_moved.clear()
	last_piece_moved = move_selection


def king_me(move_selection, player_pieces):
	if move_selection[0] == 0 or move_selection[0] == board_size - 1:
		player_pieces.pop(str(move_selection))
		player_pieces[str(move_selection)]='K'


def end_game(turn):
	break_loop = declare_winner()
	break_loop = declare_stalemate(turn, break_loop)

	return break_loop


def declare_winner():
	if len(black_pieces) == 0:
		print('X\'s win!')
		return True
	elif len(red_pieces) == 0:
		print('O\'s win!')
		return True
	else:
		return False


def declare_stalemate(turn, break_loop):
	if turn % 2 == 0:
		stalemate = no_moves_left(red_pieces, black_pieces,red_initial)
		if stalemate:
			print('No moves left. Stalemate!')
			return True
		else:
			return break_loop
	elif turn %2 != 0:
		stalemate = no_moves_left(black_pieces, red_pieces,black_initial)
		if stalemate:
			print('No no_moves_left. Stalemate!')
			return True
		else:
			return break_loop
	else:
		return break_loop



def no_moves_left(player_pieces, opponent_pieces, token):
	no_moves = True

	for piece in player_pieces:
		piece_list = convert_to_list(piece)
		if can_move(piece_list, player_pieces, opponent_pieces, token) or can_jump(piece_list, player_pieces, opponent_pieces, token):
			no_moves = False
			break

	return no_moves


def convert_to_list(string):
	back_to_list = list(string)
	back_to_list = remove_characters(back_to_list)
	new_list = convert_characters_to_numbers(back_to_list)

	return new_list


def remove_characters(back_to_list):
	checklist = ['[',']',',',' ']
	for character in checklist:
		while character in back_to_list:
			back_to_list.remove(character)

	return back_to_list


def convert_characters_to_numbers(back_to_list):
	new_list = []
	for number in back_to_list:
		new_list.append(int(number))

	return new_list


if __name__ == '__main__':
	main()
