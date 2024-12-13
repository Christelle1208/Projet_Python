import random 
       
def random_position(row, column, taken_positions):
    
    """Génère une position aléatoire unique."""
    x = random.choice(row)
    y = random.choice(column)
    while (x, y) in taken_positions:
        print("doublon")
        x = random.choice(row)
        y = random.choice(column)
    return (x, y)

PLAYER1_ROW = range(1, 5)  
PLAYER1_COLUMN = range(1, 5)  

PLAYER2_ROW = range (16,20)
PLAYER2_COLUMN = range(16,20)
