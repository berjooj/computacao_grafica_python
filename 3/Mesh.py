from OpenGL.GL import *

class Mesh:
	def __init__(self):
		self.vertices = []
		self.triangles = []
		self.draw_type = GL_POINTS

	def draw(self):
		if self.draw_type == GL_POINTS:
			glPointSize(5.0)
			glBegin(self.draw_type)
			for vertex in self.vertices:
				glVertex3fv(vertex)
			glEnd()
		elif self.draw_type == GL_LINES:
			glBegin(self.draw_type)
			for t in range(0, len(self.triangles), 3):
				for i in range(3):
					glVertex3fv(self.vertices[self.triangles[t + i]])
					glVertex3fv(self.vertices[self.triangles[t + (i + 1) % 3]])
			glEnd()
		else:
			glBegin(GL_TRIANGLES)
			for t in range(0, len(self.triangles), 3):
				glVertex3fv(self.vertices[self.triangles[t]])
				glVertex3fv(self.vertices[self.triangles[t + 1]])
				glVertex3fv(self.vertices[self.triangles[t + 2]])
			glEnd()

			glColor3f(1, 0, 0)
			glBegin(GL_LINES)
			for t in range(0, len(self.triangles), 3):
				for i in range(3):
					glVertex3fv(self.vertices[self.triangles[t + i]])
					glVertex3fv(self.vertices[self.triangles[t + (i + 1) % 3]])
			glEnd()
			glColor4f(1, 1, 1, 0.8)