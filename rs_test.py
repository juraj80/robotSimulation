from ps11 import *


room = RectangularRoom(10,10)
def test_position():
    a = Position(5.5,5.4)
    print 'getX ',a.getX()
    print 'getY ',a.getY()    
    print 'getNewPosition(45,1)'
    x = a.getNewPosition(45,1)
    print 'newX ',x.getX()
    print 'newY ',x.getY()

def test_rectangularRoom():
    
    a = Position(5.5,5.4)
    print 'cleanTileAtPosition ('+str(a.getX())+','+str(a.getY())+')' 
    room.cleanTileAtPosition(a)
    print 'room.isTileCleaned(m,n) ',room.isTileCleaned(5,5)
    print '\n'
    b = Position(6.2,5.3)
    print 'cleanTileAtPosition ('+str(b.getX())+','+str(b.getY())+')' 
    room.cleanTileAtPosition(b)
    print 'room.isTileCleaned(m,n) ', room.isTileCleaned(6,5)
    print '\n'
    print 'room.cleanedTiles ',room.cleanedTiles
    print 'room.getNumTiles ', room.getNumTiles()
    print 'room.getNumCleanedTiles ',room.getNumCleanedTiles()
    print '\n'
    print 'room.getRandomPosition()'
    c = room.getRandomPosition()
    print 'getX ',c.getX()
    print 'getY ',c.getY()
    print '\n'
    d = Position(-1.0,3.0)
    print 'room.isPositionInRoom(-1.0,3.0)'
    print room.isPositionInRoom(d)
    print '\n'
    
def test_BaseRobot():
    robot = BaseRobot(room,5)
    print 'robot.direction ',robot.direction
    print 'robot.position ',robot.position
    print 'robot.getRobotPosition() ',robot.getRobotPosition()
    print 'robot.getRobotDirection() ',robot.getRobotDirection()
    b = Position(8.2,9.3)
    print 'robot.setRobotPosition(8.2,9.3) ',robot.setRobotPosition(b)
    print 'robot.setRobotDirection(260) ',robot.setRobotDirection(260)    
    print 'robot.getRobotPosition() ',robot.getRobotPosition()
    print 'robot.getRobotDirection() ',robot.getRobotDirection()
    print '\n'
    
def test_Robot():
    roomba=Robot(room,1)
    print 'updatePositionAndClean()'
    for i in range(0,10):
        roomba.updatePositionAndClean()

def test_RandomWalkRobot():
    roomba=RandomWalkRobot(room,1)
#    roomba=Robot(room,1)
#    print 'updatePositionAndClean()'
    print dir(roomba)
   
    for i in range(0,10):
        roomba.updatePositionAndClean()


def test_runSimulation():
    list_of_lists = runSimulation(5, 1.0, 5, 5, 1.0,4,RandomWalkRobot,False)
    print 'length of result', len(list_of_lists)
    print 'computeMeans'
    print computeMeans(list_of_lists)
    print 'averageLength'
    print averageLength(list_of_lists)
        
#test_rectangularRoom()
#test_BaseRobot()
#test_Robot()
#test_RandomWalkRobot()
#test_runSimulation()
#print showPlot4()
print showPlot5()
