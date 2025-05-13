from OpenGL.GL import *
from Mesh import *
import math

class Sphere(Mesh):
	def __init__(self, radius=0.2, slices=16, stacks=16, draw_type=GL_POINTS):
		self.vertices = []
		self.triangles = []
		for i in range(stacks + 1):
			theta = i * math.pi / stacks
			sin_theta = math.sin(theta)
			cos_theta = math.cos(theta)
			for j in range(slices):
				phi = j * 2 * math.pi / slices
				sin_phi = math.sin(phi)
				cos_phi = math.cos(phi)
				x = radius * sin_theta * cos_phi
				y = radius * sin_theta * sin_phi
				z = radius * cos_theta
				self.vertices.append((x, y, z))
		for i in range(stacks):
			for j in range(slices):
				v0 = i * slices + j
				v1 = i * slices + (j + 1) % slices
				v2 = (i + 1) * slices + j
				v3 = (i + 1) * slices + (j + 1) % slices
				self.triangles.extend([v0, v2, v3])
				self.triangles.extend([v0, v3, v1])
		self.draw_type = draw_type