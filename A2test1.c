import math
import Physics

def print_object(n, object):
    if (object == None):
        print("  [%02d] = NULL;" % n)
        return
    if (object.type == Physics.STILL_BALL):
        print("  [%02d] = STILL_BALL (%d,%6.1lf,%6.1lf)" %
            (n, object.obj.still_ball.number, object.obj.still_ball.pos.x, object.obj.still_ball.pos.y))
    elif (object.type == Physics.ROLLING_BALL):
        print("  [%02d] = ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)" %
            (n, object.obj.rolling_ball.number, object.obj.rolling_ball.pos.x, object.obj.rolling_ball.pos.y,
            object.obj.rolling_ball.vel.x, object.obj.rolling_ball.vel.y, object.obj.rolling_ball.acc.x, object.obj.rolling_ball.acc.y))
    elif (object.type == Physics.HOLE):
        print("  [%02d] = HOLE (%6.1lf, %6.1lf)" % (n, object.obj.hole.pos.x, object.obj.hole.pos.y))
    elif(object.type == Physics.HCUSHION):
        print("  [%02d] = HCUSHION (%6.1lf)" % (n, object.obj.hcushion.y))
    elif (object.type == Physics.VCUSHION):
        print("  [%02d] = VCUSHION (%6.1lf)" % (n, object.obj.vcushion.x))

def print_table(table):
    if (table == None):
        print("NULL")
        return
    print("time = %6.1lf" % table.time)
    for i in range(Physics.MAX_OBJECTS):        
        print_object(i, table.get_object(i))

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

print_table(table)

while (table != None):
    #table = Physics.Table.segment(table)
    table = table.segment()
    print_table(table)
