import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Sphere import *

pygame.init()

screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 0.8)

ortho_left = -400
ortho_right = 400
ortho_bottom = -400
ortho_top = 400

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Esfera')
mesh = Sphere(radius=0.5, slices=16, stacks=16, draw_type=GL_POINTS)
rotation_angle = 0
font = pygame.font.SysFont('mono', 20)

def initialise():
	glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
	glColor4f(drawing_color[0], drawing_color[1], drawing_color[2], drawing_color[3])
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glViewport(0, 0, screen.get_width(), screen.get_height())
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glTranslate(0, 0, -5)

def draw_text():
	text_lines = [
		"3 - Mesh",
		"2 - Wireframe",
		"1 - Pontos",
		"Atalhos:"
	]
	for i, line in enumerate(text_lines):
		text = font.render(line, True, (255, 255, 255))
		text_surface = pygame.image.tostring(text, 'RGBA', True)
		text_width, text_height = text.get_size()
		glRasterPos2i(10, screen_height - 100 + i * 20)
		glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_surface)

def display():
	global rotation_angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glTranslate(0, 0, -5)
	glRotatef(rotation_angle, 1, 1, 0)
	mesh.draw()
	rotation_angle += 1

	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(0, screen_width, 0, screen_height, -1, 1)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	glDisable(GL_DEPTH_TEST)
	draw_text()
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(20, (screen_width / screen_height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	pygame.display.flip()

done = False
initialise()
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == KEYDOWN:
			if event.key == K_1:
				mesh.draw_type = GL_POINTS
			if event.key == K_2:
				mesh.draw_type = GL_LINES
			if event.key == K_3:
				mesh.draw_type = GL_TRIANGLES
	display()
	pygame.time.wait(30)
pygame.quit()