import json

with open('../configs/board.json', 'r') as f:
    data = json.load(f)

board_strings = data['boards']
boards = [[int(num) for num in row.split(',')] for row in board_strings]

with open('../configs/board2.json', 'r') as f:
    data2 = json.load(f)

board_strings2 = data2['boards']
boards2 = [[int(num) for num in row.split(',')] for row in board_strings2]

maps = [boards, boards2]
