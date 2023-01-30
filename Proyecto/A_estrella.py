import heapq
import csv

# Funcion utilizada para leer los datos de un archivo
def read_file():
    with open("Datos.txt", 'r') as file:
        csv_reader = csv.reader(file)
        list1 = []
        list2 = []
        for i, line in enumerate(csv_reader):
            line = [int(x) for x in line]
            if i < 4:
                list1.append(line)
            else:
                list2.append(line)
        return list1, list2


# Clase Estado: Representa un estado del tablero.
class State:
    def __init__(self, board, g, h, parent=None):
        self.board = board
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        
    def __lt__(self, other):
        return self.f < other.f

# Retorna la posición de el espacio en blanco en el tablero
def blank_pos(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return (i, j)
    return None


# Retorna las posibles acciones del estado actual
def actions(board):
    i, j = blank_pos(board)
    actions = []
    if i > 0:
        actions.append('up')
    if i < 3:
        actions.append('down')
    if j > 0:
        actions.append('left')
    if j < 3:
        actions.append('right')
    return actions

# Genera un nuevo tablero dependiendo del parametro de acción
def result(board, action):
    i, j = blank_pos(board)
    new_board = [row[:] for row in board]
    if action == 'up':
        new_board[i][j], new_board[i-1][j] = new_board[i-1][j], new_board[i][j]
    elif action == 'down':
        new_board[i][j], new_board[i+1][j] = new_board[i+1][j], new_board[i][j]
    elif action == 'left':
        new_board[i][j], new_board[i][j-1] = new_board[i][j-1], new_board[i][j]
    elif action == 'right':
        new_board[i][j], new_board[i][j+1] = new_board[i][j+1], new_board[i][j]
    return new_board

# Calcula la distancia Manhattan entre el estado actual y el final
def manhattan(board, final_board):
    h = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != final_board[i][j]:
                h += 1
    return h

# Implementacion de algoritmo A*
def a_star(initial_board, final_board):
    heap = []
    # Agregar al heap el estado inicial, junto con el valor de la heuristica
    heapq.heappush(heap, State(initial_board, 0, manhattan(initial_board, final_board)))
    visited = set() # Variable que almacena los estados visitados
    while heap:
        current_state = heapq.heappop(heap)
        if current_state.board == final_board:
            return current_state
        visited.add(tuple(map(tuple, current_state.board))) # Agregar estado actual a estados visitados
        for action in actions(current_state.board):
            new_board = result(current_state.board, action) # Genera un nuevo estado para cada acción posible
            if tuple(map(tuple, new_board)) not in visited: # Se asegura que el nuevo estado no haya sido visitado
                g = current_state.g + 1
                h = manhattan(new_board, final_board)
                heapq.heappush(heap, State(new_board, g, h, current_state))
    return None

# Funcion usada para encontrar el camino definido por el algorimto A*
def get_move_direction(before,after):
    for i in range(4):
        for j in range(4):
            if before[i][j]!=after[i][j]:
                if i>0 and before[i-1][j]==0:
                    return "D"
                if i<3 and before[i+1][j]==0:
                    return "U"
                if j>0 and before[i][j-1]==0:
                    return "R"
                if j<3 and before[i][j+1]==0:
                    return "L"

# Ejecución del Programa

initial_board, final_board = read_file()
result = a_star(initial_board, final_board)

if result is not None:
    path = []
    move_directions = []
    state = result
    while state.parent is not None:
        path.append(state.board)
        state = state.parent
    path.append(initial_board)
    path.reverse()
    print("Pasos para llegar al tablero final: ")
    for i in range(len(path)):
        if i>0:
            move_directions.append(get_move_direction(path[i-1],path[i]))
    for direction in move_directions:
        print(direction, end=",")
else:
    print("No se encontró una solución.")