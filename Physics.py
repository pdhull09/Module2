import phylib;
import os;
import sqlite3;
import math
FRAME_RATE= 0.01
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
    def svg(self):
        """
        Returns the SVG representation of a StillBall object.
        """
        return f"""<circle cy="%d" cx="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.y, self.obj.still_ball.pos.x, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]);






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

    def svg(self):
        """
        Returns the SVG representation of a RollingBall object.
        """
        return f"""<circle cy="%d" cx="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.y, self.obj.rolling_ball.pos.x, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number]);

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
    def svg(self):
        return f"""<circle cx="{self.obj.hole.pos.x}" cy="{self.obj.hole.pos.y}" r="{HOLE_RADIUS}" fill="black" />\n"""

######################################################################################


## Hcushion class  here
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
        y = -25 if self.obj.hcushion.y == 0 else 2700
        return f"""<rect width="1400" height="25" x="-25" y="{y}" fill="darkgreen" />\n"""


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
        x = -25 if self.obj.vcushion.x == 0 else 1350
        return f"""<rect width="25" height="2750" x="{x}" y="-25" fill="darkgreen" />\n"""
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
        for i,object in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,object);  # append object description
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
        for object in self:
            if object is not None:
                svg_string += object.svg()
        svg_string += FOOTER

        return svg_string

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            elif isinstance( ball, StillBall ):
                 # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                      Coordinate( ball.obj.still_ball.pos.x,
                                                  ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def findCueBall(self):
        # Finding and returning cue Ball from the table
        for obj in self:
            if isinstance(obj, StillBall) and obj.obj.still_ball.number==0:
                return obj
            elif isinstance(obj, RollingBall) and obj.obj.rolling_ball.number==0:
                return obj
        return None
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
        self.cur.execute("""CREATE TABLE Shot (SHOTID INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                    PLAYERID INTEGER NOT NULL,
                    GAMEID INTEGER NOT NULL,
                    FOREIGN KEY (PLAYERID) REFERENCES Player (PLAYERID),
                    FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID))""")

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
       # self.cur.close()
        self.conn.commit()

    def readTable(self, tableID):

        SQLquery = f""" SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL, TTable.TIME
                        FROM Ball
                        JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
                        JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                        WHERE BallTable.TABLEID = {tableID + 1}
                         """


        balls_info = self.cur.execute(SQLquery).fetchall();

        if not balls_info:
            return None;

        table = Table();

        table.time = balls_info[0][-1]  #  last row is Time

        for ball in balls_info:
            _, ball_no, x_coord, y_coord, x_vel, y_vel, _ = ball  # added _ to include BALLNO in correct ordering (From internet)

            if x_vel !=0 and y_vel != 0:
                Ball = RollingBall(ball_no, Coordinate(x_coord, y_coord), Coordinate(x_vel, y_vel), Coordinate(0, 0)); # constructor function Note BAll not ,ball different


            elif x_vel == 0 and y_vel == 0:
                Ball = StillBall(ball_no, Coordinate(x_coord, y_coord));
             # Using ball_no for colour

            table +=  Ball

        return table

    def writeTable(self, table):

        self.cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,)) # inserting time
        table_id_no = self.cur.lastrowid

        for object in table:

            # check --- rolling ball
            if isinstance(object, RollingBall):

                x_pos = object.obj.rolling_ball.pos.x;
                y_pos = object.obj.rolling_ball.pos.y;
                x_vel = object.obj.rolling_ball.vel.x;
                y_vel = object.obj.rolling_ball.vel.y;
                ball_no = object.obj.rolling_ball.number
                self.cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)", (ball_no, x_pos, y_pos, x_vel, y_vel))

                ball_id_no = self.cur.lastrowid
                self.cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?,?)",(ball_id_no,table_id_no));


            # check -- stillBall

            elif isinstance(object, StillBall):
                x_pos = object.obj.still_ball.pos.x;
                y_pos= object.obj.still_ball.pos.y;
                ball_no = object.obj.still_ball.number;
                y_vel=0;
                x_vel=0;

                self.cur.execute("INSERT INTO Ball (BALLNO, XPOS, XVEL, YPOS, YVEL) VALUES (?, ?, ?, ?, ?)", (ball_no, x_pos, x_vel, y_pos, y_vel));

                ball_id_no = self.cur.lastrowid;
                self.cur.execute("INSERT INTO BallTable ( TABLEID,BALLID) VALUES (?, ?)", (table_id_no,ball_id_no,));



        self.conn.commit()
        return table_id_no  # returning taable id , function looks good now !

    def close(self):
        self.conn.commit()  # simple function definition
        self.conn.close()

    def get_Info_from_GameID(self, gameID):
        # Retrieve game details using join across Game and Player tables
        Query = """ SELECT  gm.GAMENAME, p1.PLAYERNAME as Player1, p2.PLAYERNAME as Player2
                    FROM Game gm
                    JOIN Player p1 ON gm.GAMEID = p1.GAMEID
                    JOIN PLAYER p2 ON gm.GAMEID = p2.GAMEID
                    WHERE gm.GAMEID = ? AND p1.PLAYERID < p2.PLAYERID
                    ORDER BY p1.PLAYERID ASC , p2.PLAYERID ASC
                    """
        data = self.cur.execute(Query, (gameID, )).fetchone() # tuple with ( gamename , PLayer1Name, Player2Name)
        if data:
            return data
        else:
            return None, None ,None

    def createGamewithPlayers(self,gameName, player1Name, player2Name):
        #inserting new game into Game table
        self.cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = self.cur.lastrowid

        #inserting first player
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
        #inserting 2 player
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))
        self.conn.commit()
        return gameID

    def getGame (self, gameID):
        Query = f"""
        SELECT Game.GAMENAME, P1.PLAYERNAME as Player1, P2.PLAYERNAME as Player2
        FROM Game
        JOIN Player P1 ON Game.GAMEID= P1.GAMEID AND P1.PLAYERID = (
            SELECT MIN(PLAYERID) FROM Player WHERE GAMEID = {gameID+1}
        )
        JOIN Player P2 ON Game.GAMEID= P2.GAMEID AND P2.PLAYERID = (
            SELECT MAX(PLAYERID) FROM Player WHERE GAMEID = {gameID+1}
        )
        WHERE Game.GAMEID ={gameID+1}
        """
        result=self.cur.execute(Query).fetchone()
        if result:
            return result
        else:
            return None, None, None

    def setGame(self, gameName, player1Name,player2Name):
        self.cur.execute("INSERT INTO Game (GAMENAME VALUES (?)", (gameName,))
        gameID=self.cur.lastrowid
        self.cur.execute("INSERT INTO Player (GAMEID,PLAYERNAME) VALUES (?,?)", (gameID, player1Name))
        self.cur.execute("INSERT INTO Player (GAMEID,PLAYERNAME) VALUES (?,?)", (gameID, player2Name))
        self.conn.commit()
        return gameID-1 #adjust for zero based index

    def getPlayerID(self, gameID, playerName):
        Query= """
               SELECT PLAYERID FROM Player WHERE GAMEID = ? AND PLAYERNAME = ?
            """
        try:
            self.cur.execute(Query, (gameID, playerName))
            result = self.cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving player ID:{e}")
            return None;

    def recordTableShot(self,tableID, shotID):
        try:
            self.cur.execute("INSERT INTO Tableshot(TABLEID, SHOTID) VALUES (?, ?)", (tableID, shotID))
            self.conn.commit()
            return shotID
        except Exception as e:
            print(f"Issue in recordTableshot : {e}")

    def newShot(self, gameID, playerID):
        Query=""" INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)
                """

        try:
            self.cur.execute(Query, (playerID, gameID))
            self.conn.commit()
            return self.cur.lastrowid
        except Exception as e:
            return None;

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Game class implemented here now

class Game:

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None, ):

        self.db = Database()
        print("GAME initialised !!! ")

        if gameID is not None :
            print(f"Starting wioth game id : {gameID}")
            self.gameID = gameID
            details = self.db.get_Info_from_GameID(gameID)
            if details:
                self.gameName, self.player1Name, self.player2Name = details
                print(f"Game loaded : {self.gameName}, PlayerNAmes : {self.player1Name}, {self.player2Name}")
            else:
                print("Given GameID not found ")
                raise ValueError("Given GameID not found ")

        elif all([gameName, player1Name, player2Name]):
            print("")
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            self.gameID = self.db.createGamewithPlayers(gameName, player1Name, player2Name)
        else:
            raise TypeError("Invalid combination of arguments provided to the constructor.")

        self.table = None  # table initialisation



    def shoot(self, gameName, playerName, table, xvel, yvel):

        # checking if game name matches
        if gameName != self.gameName:
            raise ValueError(f"The game {gameName} does not match with this game session .")

        # Validating player ID
        playerID= self.db.getPlayerID(self.gameID, playerName)
        if playerID is None:
            raise ValueError(f"Player {playerName} not found in game")

        # Recording a new shot in database
        shotID=self.db.newShot(self.gameID, playerID)
        print(f"New shot ID: {shotID}")
        print("before calculations")
        print(table)

        #Finding cueball
        cue_ball = table.findCueBall()
        if cue_ball is None:
            raise ValueError("cue ball not found ")
        print("cue ball - ")
        print(cue_ball)

        # Updating cueBall data now

        cue_ballX = cue_ball.obj.still_ball.pos.x
        cue_ballY = cue_ball.obj.still_ball.pos.y

        cue_ball.type = phylib.PHYLIB_ROLLING_BALL;

        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel
        cue_ball.obj.rolling_ball.pos.x = cue_ballX
        cue_ball.obj.rolling_ball.pos.y = cue_ballY

        speed = math.sqrt(xvel**2 + yvel**2)
        accX=0.0
        accY=0.0
        if speed > FRAME_RATE:
            accX= -(xvel/speed)*DRAG
            accY = -(yvel/speed)* DRAG
        else:
            accX=0
            accY=0
        cue_ball.obj.rolling_ball.acc.x=accX
        cue_ball.obj.rolling_ball.acc.y=accY
        print("Cue ball after calculation")
        print(cue_ball)

        initialTableID= self.db.writeTable(table)
        self.db.recordTableShot(initialTableID, shotID)

        print("PRocessing segments ...")

        oldTime=table.time

        while table is not None:
            seg=table.segment()
            if seg is None:
                break
            newTime = seg.time
            loopTime = math.floor((newTime-oldTime) / 0.01)

            for k in range(loopTime):
                lTime = k*FRAME_RATE
                copyTable = table.roll(lTime)
                copyTable.time=oldTime+ lTime

                tId = self.db.writeTable(copyTable)
                self.db.recordTableShot(tId, shotID)

            table = seg
            oldTime = table.time












