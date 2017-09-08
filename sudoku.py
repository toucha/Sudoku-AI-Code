
#1. utils.py ----------------------------
#1.1 define rows: 
rows = 'ABCDEFGHI'

#1.2 define cols:
cols = '123456789'

#1.3 cross(a,b) helper function to create boxes, row_units, column_units, square_units, unitlist
def cross(a, b):
	return [s+t for s in a for t in b]

#1.4 create boxes
boxes = cross(rows, cols)

#1.5 create row_units
row_units = [cross(r, cols) for r in rows]

#1.6 create column_units
column_units = [cross(rows, c) for c in cols]

#1.7 create square_units for 9x9 squares
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#1.8 create unitlist for all units
unitlist = row_units + column_units + square_units

#1.9 create peers of a unit from all units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#1.10 display function receiving "values" as a dictionary and display a 9x9 suduku board
'''
Display the values as a 2-D grid.
Input: The sudoku in dictionary form
Output: None
'''
def display(values):
	width = 1+max(len(values[s]) for s in boxes)
	line = '+'.join(['-'*(width*3)]*3)
	for r in rows:
		print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
						for c in cols))
		if r in 'CF': print(line)
	return
    

#2. function.py ----------------------------
'''
Instruction: create grid_values(grid) A function to convert the string representation 
of a puzzle into a dictionary form.
'''
#2.1 grid_values function (input> strong of sudoku problem, output> dictionary of a suduku with corresponding boxes) 
#from utils import *  #remove this when use as a file
def grid_values(grid):
# In this function, you will take a sudoku as a string
# and return a dictionary where the keys are the boxes,
# for example 'A1', and the values are the digit at each
# box (as a string) or '.' if the box has no value
# assigned yet.
	result = {}
	for index, value in enumerate(grid):
		result[boxes[index]] = '123456789' if value == '.' else value
	return result

'''
Eliminate values from peers of each box with a single value.

Go through all the boxes, and whenever there is a box with a single value,
eliminate this value from the set of values of all its peers.

Args:
	values: Sudoku in dictionary form.
	Returns:
	Resulting Sudoku in dictionary form after eliminating values.
'''

def eliminate(values):
	for key, value in values.items():
		if len(value) == 1:
			for peer in peers[key]:
				result = ''
				for number in values[peer]:
					if number != value:
						result += number
				values[peer] = result
	return values

"""
Finalize all values that are the only choice for a unit.

Go through all the units, and whenever there is a unit with a value
that only fits in one box, assign the value to this box.

Input: Sudoku in dictionary form.
Output: Resulting Sudoku in dictionary form after filling in only choices.
"""

def only_choice(values):
	for key, value in values.items():
		if len(value) > 1:
			result = value
			for number in value:
				if number_exists_in_peer(key, number, values):
					result = number
					break
			values[key] = result
	return values

def number_exists_in_peer(key, number, values):
	#transform key into row number and column number where 0 is the first row/column
	row = ord(key[0])-65
	column = int(key[1])-1
	box = 3*int(row/3) + int(column/3)
	#check box
	flag = True
	for peer in square_units[box]:
		if peer == key:
			continue
		if number in values[peer]:
			flag = False
			break
	if flag:
		return True
	#check row
	flag = True
	for peer in row_units[row]:
		if peer == key:
			continue
		if number in values[peer]:
			flag = False
			break
	if flag:
		return True
	#check column
	flag = True
	for peer in column_units[column]:
		if peer == key:
			continue
		if number in values[peer]:
			flag = False
	return flag

"""
Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
If the sudoku is solved, return the sudoku.
If after an iteration of both functions, the sudoku remains the same, return the sudoku.
Input: A sudoku in dictionary form.
Output: The resulting sudoku in dictionary form.
"""

def reduce_puzzle(values):
	previous_size = 0
	while is_valid_sudoku_board(values):
		current_size = sudoku_board_size(values)
		if current_size == 81:
			#correct answer
			return values
		elif current_size == previous_size:
			#failed to eliminate anymore
			return values
		else:
			values = eliminate(values)
			values = only_choice(values)
			previous_size = current_size
	return False

def is_valid_sudoku_board(values):
	for key, value in values.items():
		if len(value) < 1:
			return False
	return True

def sudoku_board_size(values):
	size = 0
	for key, value in values.items():
		size = size + len(value)
	return size

def search(values):
	"Using depth-first search and propagation, create a search tree and solve the sudoku."
	# First, reduce the puzzle using the previous function
	# Search and Choose one of the unfilled squares with the fewest possibilities
	# Now use recursion to solve each one of the resulting sudokus, 
	# and if one returns a value (not False), return that answer!
	values = reduce_puzzle(values)
	if values == False:
		return False
	target_box = ''
	min_possibilities = 10
	for key in boxes:
		if len(values[key]) == 1:
			continue
		if len(values[key]) == 2:
			target_box = key
			break
		else:
			if len(values[key]) < min_possibilities:
				min_possibilities = len(values[key])
				target_box = key
	if len(target_box) != 0:
		for value in values[target_box]:
			new_values = values.copy()
			new_values[key] = value
			#print(key, end="->")
			search_values = search(new_values)
			if search_values != False:
				return search_values
		return False
	return values

#3. Test utils.py ----------------------------  
grid_easy = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
grid_hard = '.2..........6....3.74.8.........3..2.8..4..1.6..5.........1.78.5....9..........4.'
values = grid_values(grid_hard)
print("The original Sudoku board is **********************************************")
display(values)

#4. Test function.py ----------------------------  
new_values = search(values)
print("\n")
print("After applying Depth First Search Algorithm *****************")
display(new_values)