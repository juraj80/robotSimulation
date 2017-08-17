import math
import random
import pylab
import ps11_visualize


class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
 
        self.width = width
        self.height = height
        self.cleanedTiles = []
               
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """

        xtile=int(pos.getX())
        ytile=int(pos.getY())
        
        self.cleanedTiles.append((xtile,ytile))
    

        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        for tile in self.cleanedTiles:
            if tile[0]==m and tile[1]==n:
                return True
        return False 
        
        
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height
        
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanedTiles)
    
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """

        return Position(random.uniform(0,self.width),random.uniform(0,self.height))
        
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """

        if 0<=pos.getX()<=self.width and 0<=pos.getY()<=self.height:
            return True
        else:
            return False
        


class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """

        self.room = room
        self.speed = speed
        self.direction = random.randint(0,360)
        self.position = room.getRandomPosition()
        
        
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
    
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """

        self.position = position
        
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        xdirection = self.direction
        yspeed = self.speed
        newposition = self.position.getNewPosition(xdirection,yspeed )
        newX=int(newposition.getX())
        newY=int(newposition.getY())

        if self.room.isPositionInRoom(newposition):
            if not self.room.isTileCleaned(newX,newY):
                self.room.cleanTileAtPosition(newposition)
            self.setRobotPosition(newposition)
        else:
            self.direction = random.randint(0,360)
            


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
  
    result =[]
    for trial in range(0,num_trials):
        timesteps = []
        list_of_robots=[]
        if visualize==True:
            anim = ps11_visualize.RobotVisualization(num_robots,width,height,0.2)
        room = RectangularRoom(width,height)
        for i in range(num_robots):
            robot=robot_type(room,speed)
            list_of_robots.append(robot)
        coverage = 0.0
        while coverage < min_coverage:
            for robot in list_of_robots:
                robot.updatePositionAndClean()
            if visualize==True:
                anim.update(room,list_of_robots)
            cleanTiles = float(room.getNumCleanedTiles())
            coverage = cleanTiles/room.getNumTiles()
            timesteps.append(coverage)
        result.append(timesteps)
        if visualize==True:
            anim.done()
    return result


def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """

    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    tots = pylab.array(tots)
    means = tots/float(len(list_of_lists))
    return means

def averageLength(list_of_lists):
    """
    Returns the average length of all lists in the list of lists returned by
    runSimulation
    """
    sum = 0
    result=[]
    for lst in list_of_lists:
        length = len(lst)
        sum+=length
        result.append(length)
    return float(sum)/len(result)

    

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    num_sims = 50
    min_coverage = 0.75
    roomSize = pylab.array([5,10,15,20,25])
    timeSteps = []
    for i in roomSize:
        result = runSimulation(1, 1.0, i, i, min_coverage,num_sims,Robot,False)
        timeSteps.append(averageLength(result))
  
    pylab.plot(roomSize**2,timeSteps)
    pylab.xlabel('Room area')
    pylab.ylabel('Timesteps') #Mean Time
    pylab.title('Time to clean 75% of square room with 1 robot, for various room sizes.')
    pylab.show()
    
    
def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    num_of_robots = pylab.arange(1,11)
    min_coverage = 0.75
    num_sims = 50
    timesteps = []
    for i in num_of_robots:
       result = runSimulation(i, 1.0,25,25, min_coverage,num_sims,Robot,False)
       timesteps.append(averageLength(result))

    pylab.plot(num_of_robots,timesteps)
    pylab.xlabel('Number of robots')
    pylab.ylabel('Timesteps')
    pylab.title('Time to clean 75% of  25x25 square room with 1 - 10 robots')
    pylab.show()
    
        
        
def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    roomShape = [(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    min_coverage = 0.75
    num_sims = 50
    timesteps = []
    for i in roomShape:
        result = runSimulation(2,1.0,i[0],i[1],min_coverage,num_sims,Robot, False)
        timesteps.append(averageLength(result))
    xAxis = []
    for i in roomShape:
        xAxis.append(float(i[0])/i[1])
    
    pylab.plot(xAxis,timesteps)
    pylab.xlabel('ratio of width and height')
    pylab.ylabel('Timesteps')
    pylab.title('Time to clean 75% of rooms with different room shape')
    pylab.show()
    
def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    perc_clean = pylab.arange(0.1,1.1,0.1)
    num_sims = 5
    num_of_robots = 5
    for i in range(1,num_of_robots+1):
        timesteps = []
        for j in perc_clean:
            result=runSimulation(i,1.0,5,5,j,num_sims,Robot,False)
            timesteps.append(averageLength(result))
 
        pylab.plot(perc_clean,timesteps)
        pylab.xlabel('Percentage cleaned')
        pylab.ylabel('Timesteps')
        pylab.title('Cleaning time vs. percentage cleaned, for each of 1-5 robots.')
    pylab.show()
        
       
class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        xdirection = self.direction
        yspeed = self.speed
        newposition = self.position.getNewPosition(xdirection,yspeed)
        newX=int(newposition.getX())
        newY=int(newposition.getY())
        if self.room.isPositionInRoom(newposition):
            if not self.room.isTileCleaned(newX,newY):
                self.room.cleanTileAtPosition(newposition)
            self.setRobotPosition(newposition)
        self.direction = random.randint(0,360)



def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """

    num_robots = 5
    width = 5
    height = 5
    min_coverage = 0.75
    num_trials = 10
    roomSize = pylab.array([5,10,15,20,25])
    robots = [Robot,RandomWalkRobot]
    for j in robots:
        timesteps = []
        for i in roomSize:  
            result = runSimulation(num_robots, 1.0, i, i, min_coverage, num_trials,j, False)
            timesteps.append(averageLength(result))
        pylab.plot(roomSize**2,timesteps)
        pylab.xlabel('Room Area')
        pylab.ylabel('Time Steps')
        pylab.title('Time to clean of square room with the two types of Robots.')
    pylab.show()
