import pygame
from pygame.sprite import Sprite
from pygame.locals import *
import queue
import math
import time

#python implementation fo a*

WIDTH, HEIGHT = 1000,1000

def main():
	g = Grid("map2.txt")

	b = Board(g.loadFile())

	#c = b.cells[2,1]
	#a = b.cells[5,8]

	a = b.cells[3,3]
	#c = b.cells[25,27]

	#b.getFCost(a,c)

	#cf = b.aStar(a,c)


	#for x in cf:
	#	x.color = (0,255,0)
	#print(b.dims)
	runAll(b)
	#drawBoard(b)



	print(b.printBoard())

def runAll(bIn):
	global FPS, clock, screen, WIDTH, HEIGHT
	FPS = 60
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((WIDTH,HEIGHT))
	run = True

	screen.fill((0,0,0))

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()

			if event.type == KEYDOWN:
				if event.key==K_t:
					print(bIn.drawCord)
					bIn.drawCord = not bIn.drawCord

			if event.type==pygame.MOUSEBUTTONDOWN:
				bIn.clearBoard()
				mPos = pygame.mouse.get_pos()
				cord = getCell(bIn, mPos)
				bIn.cells[cord[0],cord[1]].modified = True
				bIn.aStar(bIn.cells[3,3], bIn.cells[cord[0],cord[1]])

		
		drawBoard(bIn)
		pygame.display.update()
		clock.tick(FPS)

#method used for drawing while running a search
def itermDraw(bIn):
	global FPS, clock, screen, WIDTH, HEIGHT

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()

	drawBoard(bIn)
	pygame.display.update()
	clock.tick(FPS)

def drawBoard(bIn):
	h, w = HEIGHT//bIn.dims[0], WIDTH//bIn.dims[1]

	for i in range(bIn.dims[0]):
		for j in range(bIn.dims[1]):
			c = bIn.cells[i,j]

			if (c.modified):
				#used to draw the board this method could potentially be moved into the cell class to make things cleaner
				#attempt to only draw the cell if it is modified, this will need work.				
				pygame.draw.rect(screen, c.color, pygame.Rect((j*w)+1, (i*h)+1, c.size[0], c.size[1]))
					#c.modified = False

				#write the position of each cell currently kind of messy due to the way the screen is drawn
				#screen coords are inverted of how the matrix is stored
				if (not str(c.val).isalpha()):
					c.val = c.fCost

				font = pygame.font.SysFont(None, 24)
				img = font.render("{}".format(c.val), True, (0,0,0))
				screen.blit(img, ((j*w) + c.size[0]//2, (i*h) + c.size[1]//2))

				if bIn.drawCord:
					font2 = pygame.font.SysFont(None, 16)

					img2 = font2.render("{}".format(c.hCost), True, (0,0,0))
					screen.blit(img2, ((j*w + c.size[0]//6, (i*h) + c.size[1]//6)))

					img3 = font2.render("{}".format(c.gCost), True, (0,0,0))
					screen.blit(img3, ((j*w) + c.size[0]//2 + 20, (i*h) + c.size[1]//6))

					img4 = font2.render("{}".format(c.pos), True, (0,0,0))
					screen.blit(img4, ((j*w) + c.size[0]//6 + 20, (i*h) + c.size[1]//4))
				#pygame.draw.rect(screen, (0,0,0), pygame.Rect((i*h)+ c.size[0]//2, (j*w) + c.size[1]//2, 2, 2))
				c.modified = False

#used to retrieve the cell from given coordinates on board
#currently just changes the color to red
def getCell(bIn, cord):
	h, w = HEIGHT//bIn.dims[0], WIDTH//bIn.dims[1]
	x, y = cord[1]//h, cord[0]//w
	print("x: {} y: {}".format(cord[1]//h, cord[0]//w))
	#bIn.cells[x,y].color = (255,0,0)
	return([x,y])


class Board:

	def __init__(self, gRin):
		self.cells = {} #creates a dictioray of cells keyed to location [x,y]
		self.dims = [0,0]
		self.grin = gRin
		self.buildBoard(gRin)
		self.start = None #start cell
		self.goal = None #goal Node
		self.drawCord = False
		
		self.buildConnects()

	#given a matrix create cells at relative positions and add to dictionary
	def buildBoard(self, grin):
		self.dims = [len(grin), len(grin[0])]
		for i in range(len(grin)):
			for j in range(len(grin[i])):
				#print("i: {} j: {}".format(i,j))
				self.cells[i,j] = Cell(grin[i][j], [i,j], self.dims)

	def clearBoard(self):
		self.buildBoard(self.grin)
		self.buildConnects()

	def printBoard(self):
		stOut = ""
		for i in range(self.dims[0]):
			for j in range( self.dims[1]):
				#stOut += self.cells[i,j].val + " "
				stOut += str(self.cells[i,j].pos) + " "
			stOut += "\n"

		return(stOut)

	#gets an f and g cost for all cells
	def getFCost(self, start, goal):
		q = queue.Queue()
		start.gCost = 0
		parents = dict()
		parents[start] = None
		visited = []
		visited.append(start)

		#initialize with start to issues with getting gcost from None 
		for c in start.neighbors:
			parents[c] = start
			q.put(c)

		while(not q.empty()):
			current = q.get()
			visited.append(current)
			#calculate movement cost from start
			current.gCost = parents[current].gCost + round( (math.sqrt( (current.pos[0] - parents[current].pos[0])**2 + (current.pos[1] - parents[current].pos[1])**2 )) * 10)
			current.hCost = round( (math.sqrt( (current.pos[0] - goal.pos[0])**2 + (current.pos[1] - goal.pos[1])**2)) * 10)
			current.fCost = current.gCost + current.hCost
			#print(current.fCost)

			for n in current.neighbors:
				#itermDraw(self)
				if n not in parents:
					parents[n] = current
					q.put(n)
					#print(n.pos)

	#iterates through all items and builds a grid of their neighbors
	def buildConnects(self):
		for k in self.cells.keys():
			c = self.cells[k]
			for i in range(int(k[0])-1, int(k[0])+2):
				for j in range(int(k[1]-1), int(k[1])+2):
					if(i >= 0 and i < self.dims[0] and j >= 0 and j < self.dims[1] and self.cells[i,j] != c):
						c.neighbors.append(self.cells[i,j])

	def aStar(self, start, goal):
		Cell.__lt__ = lambda self, other : self

		frontier = queue.PriorityQueue()
		frontier.put((0, start))
		start.fCost = 0

		came_from = dict()
		came_from[start] = None

		cost_so_far = dict()
		cost_so_far[start] = 0

		while (not  frontier.empty()):
			tmp = frontier.get()
			current = tmp[1]
			#print("current pos {} cost so far {} priority {}".format(current.pos, cost_so_far[current], tmp[0]))

			if current == goal:
				break

			current.getNeighborFCost(goal)
			#itermDraw(self)

			for next in current.neighbors:
				new_cost = cost_so_far[current] + next.gCost

				if ( next.walkable and (next not in cost_so_far or new_cost < cost_so_far[next]) ):
					#print("pos {} cost {}".format(next.pos, new_cost))
					cost_so_far[next] = new_cost
					next.color = (0,0,255)
					next.modified = True

					itermDraw(self)

					priority = next.fCost
					frontier.put((priority, next))
					came_from[next] = current

		current = goal
		path = []
		while(current != start):
			current.color = (0,255,0)
			path.append(current)
			current.modified = True
			current = came_from[current]
		start.color = (0,255,0)
		path.append(start)
		path.reverse()
		return(path)


	def printParents(self, c):
		if(c.parent != None):
			self.printParents(c.parent)

class Cell:

	def __init__(self, val, pos = None, dims=None, parent=None):
		self.size = [WIDTH//dims[1] -2, HEIGHT//dims[1] - 2]
		self.val = val
		self.color = (255,255,255)
		if (val == "x"):
			self.walkable = False
			self.color = (0,0,0)
		else:
			self.walkable = True
		self.gCost = 0 #distance from starting node
		self.hCost = 0 #distance from goal node
		self.fCost = 0 #sum of g and h cost
		self.parent = parent
		self.pos = pos
		self.modified = True
		self.neighbors = []
		self.visited = False

	#cost of movement from current node
	def getNeighborGCost(self):
		for c in self.neighbors:
			if not c.visited and c.walkable:
				c.gCost = self.gCost + round( (math.sqrt( (self.pos[0] - c.pos[0])**2 + (self.pos[1]-c.pos[1])**2)) * 10)

	#calculates the H cost for each node in neighbors given a goal node
	def getNeighborHCost(self, gN):
		for c in self.neighbors:
			if not c.visited and c.walkable:
				c.hCost = round( (math.sqrt( (c.pos[0] - gN.pos[0])**2 + (c.pos[1] - gN.pos[1])**2)) * 10)

	def getNeighborFCost(self, gN):
		self.getNeighborGCost()
		self.getNeighborHCost(gN)
		for c in self.neighbors:
			if c.walkable:
				c.fCost = c.gCost + c.hCost
				c.visited = True

class Grid:

	def __init__(self, fIn):
		self.gr = []
		self.fPath = fIn
	
	#load file and return a nxm matrix
	def loadFile(self):
		f = open(self.fPath, "r")
		try:
			self.gr = [[y for y in x.split()] for x in f]
		finally:
			f.close()
		return(self.gr)

if __name__ == '__main__':
	main()