import math
import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import z_rotation

class Turtle3D:
	def __init__(self, position=(0, 0, 0), direction=(0, 1, 0)):
		self.position = np.array(position, dtype=float)
		self.direction = np.array(direction, dtype=float) / np.linalg.norm(direction)
		self.transform = np.identity(4, dtype=float)
		self.transform_stack = []
		self.line_width = 1.0

	def forward(self, length):
		new_position = self.position + self.direction * length
		glBegin(GL_LINES)
		glVertex3f(*self.position)
		glVertex3f(*new_position)
		glEnd()
		self.position = new_position

	def rotate(self, angle_deg):
		angle_rad = math.radians(angle_deg)
		self.direction = z_rotation(self.direction, angle_rad)
		rot_matrix = np.array([
			[np.cos(angle_rad), -np.sin(angle_rad), 0, 0],
			[np.sin(angle_rad), np.cos(angle_rad), 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]
		])
		self.transform = self.transform @ rot_matrix

	def push_transform(self):
		self.transform_stack.append((self.position.copy(), self.transform.copy()))

	def pop_transform(self):
		if self.transform_stack:
			self.position, self.transform = self.transform_stack.pop()
			rotation = self.transform[:3, :3]
			self.direction = rotation @ np.array([0, 1, 0], dtype=float)

	def reset(self):
		self.position = np.array([0, 0, 0], dtype=float)
		self.direction = np.array([0, 1, 0], dtype=float)
		self.transform = np.identity(4, dtype=float)
		self.transform_stack.clear()

def init_opengl(width, height):
	pygame.init()
	screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
	pygame.display.set_caption('Tagaruga')
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, width / height, 0.1, 1000.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(0, -300, 150, 0, 0, 0, 0, 0, 1)
	return screen

def run_lsystem(axiom, rules, iterations):
	result = axiom
	for _ in range(iterations):
		result = ''.join(rules.get(c, c) for c in result)
	return result

def draw_lsystem(turtle, instructions, length, angle):
	glLineWidth(turtle.line_width)
	for c in instructions:
		if c == 'F':
			turtle.forward(length)
		elif c == '+':
			turtle.rotate(angle)
		elif c == '-':
			turtle.rotate(-angle)
		elif c == '[':
			turtle.push_transform()
		elif c == ']':
			turtle.pop_transform()

def main():
	screen_width = 1000
	screen_height = 800
	screen = init_opengl(screen_width, screen_height)

	turtle = Turtle3D(position=(0, 0, 0))
	axiom = 'F'
	rules = {
		'F': 'F[+F]F[-F]F'
	}
	iterations = 3
	draw_length = 10
	angle = 25

	instructions = run_lsystem(axiom, rules, iterations)

	clock = pygame.time.Clock()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				done = True

		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glColor3f(1, 1, 1)

		turtle.reset()
		glPushMatrix()
		draw_lsystem(turtle, instructions, draw_length, angle)
		glPopMatrix()

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()

if __name__ == '__main__':
	main()