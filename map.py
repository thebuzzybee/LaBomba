from config import *

def create_empty_map():
    return [[empty for i in range(column_count)] for i in range(row_count)]

def create_map1():
    tilemap = create_empty_map()
    tilemap[0] = [indestructible for i in range(column_count)]
    tilemap[row_count - 1] = [indestructible for i in range(column_count)]
    for i in range(row_count):
        tilemap[i][0] = indestructible
        tilemap[i][column_count - 1] = indestructible
        
    for i in range(2, row_count - 1, 2):
        for j in range(2, column_count - 1, 2):
            tilemap[i][j] = indestructible
    
    for i in tilemap:
        if i == empty:
            
        
            
    tilemap[1][1] = player1
    tilemap[1][2] = empty
    tilemap[2][1] = empty
    tilemap[1][column_count - 2] = player2
    tilemap[1][column_count - 3] = empty
    tilemap[2][column_count - 2] = empty
    tilemap[row_count - 2][1] = empty
    tilemap[row_count - 2][2] = empty
    tilemap[row_count - 3][1] = empty
    tilemap[row_count - 2][column_count - 2] = empty
    tilemap[row_count - 2][column_count - 3] = empty
    tilemap[row_count - 3][column_count - 2] = empty
    
    
    return tilemap