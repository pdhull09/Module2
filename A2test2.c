import math
import Physics

def write_svg_to_file(n, table):
    if table is None:
        return
    with open(f'table-{n}.svg', 'w') as f:
        f.write(table.svg())

table = Physics.Table()
x = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)
y = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)
pos = Physics.Coordinate(x, y)
sb = Physics.StillBall(1, pos)

pos_x = Physics.TABLE_WIDTH / 2.0
pos_y = Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0
pos = Physics.Coordinate(pos_x, pos_y)
vel_x = 0.0
vel_y = -1000.0     # 1m/s (medium speed)
vel = Physics.Coordinate(vel_x, vel_y)
acc_x = 0.0
acc_y = 180.0
acc = Physics.Coordinate(acc_x, acc_y)
rb = Physics.RollingBall(0, pos, vel, acc)

table += sb
table += rb

i = 0
write_svg_to_file(i, table)

while table is not None:
    table = table.segment()
    i += 1
    
    write_svg_to_file(i, table)
