import phylib;
import os;
import sqlite3;
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;
DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;


# add more here

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_STILL_BALL,
                                       number,
                                       pos, None, None,
                                       0.0, 0.0 );

        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self, BALL_RADIUS, BALL_COLOURS):
        return f'<circle cx="{self.pos[0]}" cy="{self.pos[1]}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.number]}" />\n'




################################################################################

# RollingBall Class here

class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y), and acceleration (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0)

        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall

    # add an svg method here
    def svg(self, BALL_RADIUS, BALL_COLOURS):
        return f'<circle cx="{self.pos[0]}" cy="{self.pos[1]}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.number]}" />\n'

###########################################################################################

## Hole class here
class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        """
        Constructor function. Requires position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      None,
                                      pos, None, None,
                                      0.0, 0.0)

        # this converts the phylib_object into a Hole class
        self.__class__ = Hole
    # SVG method here
    def svg(self, HOLE_RADIUS):
        return f'<circle cx="{self.pos[0]}" cy="{self.pos[1]}" r="{HOLE_RADIUS}" fill="black" />\n'

######################################################################################

## Hcushion class  here
class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires y-coordinate as
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      None,
                                      None, None, None,
                                      y, 0.0)

        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion

    # SVG method here
    def svg(self):
        y = -25 if self.y == 0 else 2700
        return f'<rect width="1400" height="25" x="-25" y="{y}" fill="darkgreen" />\n'
#--------------------------------------------------------------------------------------

# Vcushion class here
class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires x-coordinate as
        argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      None,
                                      None, None, None,
                                      x, 0.0)

        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion
    # SVG method here
    def svg(self):
        x = -25 if self.x == 0 else 1350
        return f'<rect width="25" height="2750" x="{x}" y="-25" fill="darkgreen" />\n'
#--------------------------------------------------------------------------------------

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index );
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        """
        Creates a string that consists of the concatenation of:
        1. HEADER,
        2. The return values of the svg method called on every object in the Table.
        3. FOOTER.
        The method returns the string.
        """
        svg_string = HEADER
        for obj in self:
            if hasattr(obj, 'svg'):
                svg_string += obj.svg()
        svg_string += FOOTER

        return svg_string
#----------------------------------------------------------------------------------------------------------------------
# New Code here for A3
class Database:
    def __init__(self, reset=False):
        if reset:
            db_file = "phylib.db"
            if os.path.exists(db_file):
                os.remove(db_file)

        self.conn = sqlite3.connect("phylib.db")
        self.cur = self.conn.cursor()

    def createDB( self):
        # creating tables for the database now
        # table 1 Ball

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Ball (
                            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BALLNO INTEGER NOT NULL,
                            XPOS FLOAT NOT NULL,
                            YPOS FLOAT NOT NULL,
                            XVEL FLOAT,
                            YVEL FLOAT
                            )""")

        # table 2 TTable
        self.cur.execute("""CREATE TABLE IF NOT EXISTS TTable (
                            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            TIME FLOAT  NOT NULL
                            )""")

        # table 3 BallTable
        self.cur.execute('''CREATE TABLE IF NOT EXISTS BallTable (
                            BALLID INTEGER NOT NULL,
                            TABLEID INTEGER NOT NULL,
                            FOREIGN KEY(BALLID) REFERENCES Ball (BALLID),
                            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID)
                            )''')

        # table 4 Shot
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Shot (
                         SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                         PLAYERID INTEGER NOT NULL,
                         GAMEID INTEGER NOT NULL
                         FOREIGN  KEY(PLAYERID) REFERENCES Player(PLAYERID),
                         FOREIGN  KEY(GAMEID) REFERENCES Game(GAMEID)
                         )''')

        # table 5 TableShot
        self.cur.execute('''CREATE TABLE IF NOT EXISTS TableShot (
                         TABLEID INTEGER NOT NULL,
                         SHOTID INTEGER NOT NULL,
                         FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID),
                         FOREIGN  KEY(SHOTID) REFERENCES Shot(SHOTID)
                         )''')

        # TABLE 6 Game
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Game(
                            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMENAME VARCHAR(64) NOT NULL
                         )''')

        # Table 7 Player
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Player(
                         PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                         GAMEID  INTEGER NOT NULL,
                         PLAYERNAME VARCHAR(64) NOT  NULL,
                         FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                         )''')
        # closing connection and commiting now
        self.cur.close()
        self.conn.commit()

    def readTable(self, tableID):
        self.cur = self.conn.cursor()
        self.cur.execute("""
        SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL, TTable.TIME
        FROM BallTable
        JOIN Ball ON BallTable.BALLID = Ball.BALLID
        JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
        WHERE BallTable.TABLEID = ?
        """, (tableID + 1,))

        rows = self.cur.fetchall()
        self.cur.close()

        if not rows:
            return None

        table = Table()  # Initialize a Table object
        for row in rows:
            ball_id, ball_no, xpos, ypos, xvel, yvel, time = row
            if xvel is None and yvel is None:
                ball = StillBall(ball_no, (xpos, ypos))  # Instantiate StillBall object
            else:
                vel = (xvel, yvel)
                acc = None  # Assuming acceleration is not provided in the database
                ball = RollingBall(ball_no, (xpos, ypos), vel, acc)  # Instantiate RollingBall object
                # Set the acceleration of the ball as per your A2 requirements
                # ball.set_acceleration(...)

            table += ball  # Add ball object to the table

        # Add the standard holes and cushions to the table as per your A2 requirements
        # Assuming you have predefined positions for holes and cushions
        table += Hole((0, 0))  # Example position for hole
        table += HCushion(0)   # Example position for horizontal cushion
        table += VCushion(0)   # Example position for vertical cushion

        table.time = time  # Set the table's time attribute
        return table  # Return the populated Table object

    def writeTable(self, table):
        """
        This method stores the contents of the Table class object named table in the database.
        """
        # Insert into TTable
        self.cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = self.cur.lastrowid - 1  # Adjusting for zero-indexing

        # Insert into Ball and BallTable
        for ball in table.balls:
            self.cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",
                             (ball.ballno, ball.xpos, ball.ypos, ball.xvel, ball.yvel))
            ball_id = self.cur.lastrowid
            self.cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))

        # Commit changes and return table_id
        self.conn.commit()
        return table_id
#---------------------------------------------------------------------------------------------------------------
# Game class implemented here now

class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None, table=None):
        self.db = Database()
        if gameID is not None and all(arg is None for arg in [gameName, player1Name, player2Name, table]):
            self.gameID = gameID + 1  # Adjusting for zero-indexing
            self.getGame()  # Retrieve game details from the database
        elif gameID is None and all(arg is not None for arg in [gameName, player1Name, player2Name, table]):
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.table = table
            self.setGame()  # Add new game details to the database
        else:
            raise TypeError("Invalid combination of arguments provided to the constructor.")

    def getGame(self):
        # Retrieve game details from the database using a helper method in the Database class
        self.gameName, self.player1Name, self.player2Name = self.db.getGame(self.gameID)
        self.table = self.db.readTable(self.gameID)

    def setGame(self):
        # Add new game details to the database using a helper method in the Database class
        self.gameID = self.db.setGame(self.gameName, self.player1Name, self.player2Name)
        self.db.writeTable(self.table)

    def shoot(self, gameName, playerName, table, xvel, yvel):
        # Add a new entry to the Shot table for the current game and the given playerID
        shotID = self.db.newShot(gameName, playerName, table, xvel, yvel)
        return shotID
