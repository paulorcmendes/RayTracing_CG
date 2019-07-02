import cv2
import numpy as np

import loadObj
from loadObj import *
		
def rayTrace(p0, p1, faces):

	#vetor u
	raio = Vec3(p1.x-p0.x, p1.y-p0.y, p1.z-p0.z)

	for face in faces:
		normal_plano = face.normals[0]
		#ha intersecao
		if vectorialProd(raio, normal_plano) != 0:
			k = vectorialProd(normal_plano, face.vertices[0])
			t = (k - vectorialProd(normal_plano, p0))/(vectorialProd(normal_plano, raio))
			#intersecao do plano com o raio
			p_plano = Vec3(p0.x + t*raio.x, p0.y+ t*raio.y, p0.z+t*raio.z)

			length_vertices = len(face.vertices)
			ang = 0
			for i in range(length_vertices):
				i_next = (i+1)%length_vertices

				vet1 = sub(face.vertices[i], p_plano)
				vet2 = sub(face.vertices[i_next], p_plano)
				ang += angulo(vet1, vet2)
			#print(ang)
			if(abs(360-ang) < 2):
				return 1

			#print(p_plano.toString())

	return 0		

print("Hello World")

vertices, normals, faces = loadObj.readObj("Charizard.obj")

new_faces = []

for face in faces:
	if face.normals[0].z < 0:
		new_faces.append(face)
faces = new_faces

lin = 200
cols = 200

COP = Vec3(0,0,-50)
xmin = -2
ymin = -2
xmax = 2
ymax = 2

dist = -45
width = (xmax-xmin)/cols
height = (ymax-ymin)/lin

image = np.zeros((lin, cols))

for i in range(lin):
	print(i)
	for j in range(cols):
		p0 = COP
		p1 = Vec3(xmin+width*(j+0.5), ymax-height*(i+0.5), dist)
		image[i,j] = rayTrace(p0, p1, faces)

print(image)
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()