import random
import time
import os

#---------------------------------------------------------------------------

def initialise_grid(columns, rows, array):
	for i in range(rows):
		array_row = []
		for j in range(columns):
			if (i == 0 or j == 0 or (i == rows - 1) or (j == columns - 1)):
				array_row += [-1]
			else:
				ran = random.randint(0,3)
				if ran == 0:
					array_row += [1]
				else:
					array_row += [0]
		array += [array_row]

#---------------------------------------------------------------------------
    
def print_gen(columns, rows, array, gen_no):
	os.system("cls")

	print("Game of Life -- Generation " + str(gen_no + 1))
    
	for i in range(rows):
		for j in range(columns):
			if array[i][j] == -1:
				print("#", end=" ")
			elif array[i][j] == 1:
				print(".", end=" ")
			else:
				print(" ", end=" ")
		print("\n")

#---------------------------------------------------------------------------

def process_next_gen(columns, rows, current, next):
	for i in range(1,rows-1):
		for j in range(1,columns-1):
			next[i][j] = process_neighbours(i, j, current)

#---------------------------------------------------------------------------
      
def process_neighbours(x, y, array):
	count = 0
	for j in range(y-1,y+2):
		for i in range(x-1,x+2):
			if not(i == x and j == y):
				if array[i][j] != -1:
					count += array[i][j]
	if array[x][y] == 1 and count < 2: return 0
	if array[x][y] == 1 and count > 3: return 0
	if array[x][y] == 0 and count == 3: return 1
	else: return array[x][y]

#---------------------------------------------------------------------------
############################################################################
#---------------------------------------------------------------------------

ROWS = 11
COLS = 39
GENERATIONS = 100
DELAY = 0.2

this_gen = []
next_gen = []

initialise_grid(COLS, ROWS, this_gen)
initialise_grid(COLS, ROWS, next_gen)

for gens in range(GENERATIONS):
	print_gen(COLS, ROWS, this_gen, gens)
	process_next_gen(COLS, ROWS, this_gen, next_gen)
	time.sleep(DELAY)
	this_gen, next_gen = next_gen, this_gen
input("Finished. Press <return> to quit.")
