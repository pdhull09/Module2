import json
from Physics import Coordinate, StillBall, Table, Hole

# constants
BALL_RADIUS = 28.5
BALL_DIAMETER = 2*BALL_RADIUS
HOLE_RADIUS = 2* BALL_DIAMETER
TABLE_LENGTH = 2700.0
TABLE_WIDTH = TABLE_LENGTH / 2.0

def initialize_table_with_balls():
    table=Table()

    # add the cueball
    cue_ball_pos = Coordinate(TABLE_WIDTH/4, TABLE_LENGTH /  2)
    cue_ball = StillBall(0,cue_ball_pos)
    table += cue_ball

    # set up other balls in a triangle formation
    apex_x = 3* TABLE_WIDTH / 4
    apex_y = TABLE_LENGTH / 2
    horizontal_gap= 4
    vertical_gap = 205
    row_length=BALL_DIAMETER + horizontal_gap

    # Loop to place balls in triangle
    ball_number = 1
    for row in range(1,6):
        for col in range(row):
            pos_x = apex_x -((row - 1) * row_length / 2) + (col * row_length)
            pos_y = apex_y + ((row -1 ) * (BALL_DIAMETER + vertical_gap) * (3**0.5) / 2)
            ball = StillBall(ball_number, Coordinate(pos_x, pos_y))
            table += ball
            ball_number +=1

    # hole adding
    table += Hole(Coordinate(HOLE_RADIUS, HOLE_RADIUS)) # to-left
    table += Hole(Coordinate(TABLE_WIDTH - HOLE_RADIUS, HOLE_RADIUS))
    table += Hole (Coordinate(HOLE_RADIUS, TABLE_LENGTH - HOLE_RADIUS))
    table += Hole(Coordinate(TABLE_WIDTH - HOLE_RADIUS, TABLE_LENGTH- HOLE_RADIUS))
    return table

def save_game_state(table):
    game_state = {
        "table": table.to_json(),

    }
    with open('game_state.json', 'w') as f:
        json.dump(game_state, f)

def save_svg(table, filename):
    with open(filename, 'w') as f:
        f.write(table.svg())
if __name__ == "__main__":
    table =initialize_table_with_balls()
    save_svg(table, 'initial_table.svg')
