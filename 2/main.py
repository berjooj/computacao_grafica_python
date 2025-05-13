import math
import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Utils import z_rotation

pygame.init()

screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

ortho_left = -400
ortho_right = 400
ortho_bottom = -400
ortho_top = 400

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Lindenmayer - Turtle')

current_position = (0, -200)
direction = np.array([0, 1, 0], dtype=float)
draw_length = 5
rule_run_number = 4
axiom = 'F'
rules = {
	'F': 'F[+F]F[-F]F'
}
angle = 25
stack = []
instructions = ''

def run_rule(run_count):
	global instructions
	instructions = axiom
	for _ in range(run_count):
		old_system = instructions
		instructions = ''
		for c in old_system:
			instructions += rules.get(c, c)

def init_ortho():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(ortho_left, ortho_right, ortho_bottom, ortho_top)

def reset_turtle():
	global current_position, direction
	glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glColor4f(drawing_color[0], drawing_color[1], drawing_color[2], drawing_color[3])
	glLoadIdentity()
	current_position = (0, -200)
	direction = np.array([0, 1, 0], dtype=float)
	stack.clear()
	move_to(current_position)

def draw_turtle():
	global current_position, direction
	for c in instructions:
		if c == 'F':
			forward(draw_length)
		elif c == '+':
			rotate(angle)
		elif c == '-':
			rotate(-angle)
		elif c == '[':
			stack.append((current_position, direction.copy()))
		elif c == ']':
			pos, dir = stack.pop()
			move_to(pos)
			direction = dir

def move_to(pos):
	global current_position
	current_position = (pos[0], pos[1])

def line_to(x, y):
	global current_position
	glBegin(GL_LINES)
	glVertex2f(current_position[0], current_position[1])
	glVertex2f(x, y)
	glEnd()
	current_position = (x, y)

def forward(length):
	new_x = current_position[0] + direction[0] * length
	new_y = current_position[1] + direction[1] * length
	line_to(new_x, new_y)

def rotate(angle):
	global direction
	direction = z_rotation(direction, math.radians(angle))

init_ortho()
glLineWidth(1.0)
run_rule(rule_run_number)

done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				done = True

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	reset_turtle()
	draw_turtle()
	pygame.display.flip()

pygame.quit()