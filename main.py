import cv2
import numpy as np

import loadObj
from loadObj import *
		

luzAmbiente = [1,1,1]


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
			#ponto esta na face
			if(abs(360-ang) < 2):
				k_reflex = [0, 0.2, 1]

				return k_reflex[0]*luzAmbiente[0], k_reflex[1]*luzAmbiente[1], k_reflex[2]*luzAmbiente[2]

			#print(p_plano.toString())

	return 0,0,0		

print("Hello World")

vertices, normals, faces = loadObj.readObj("LowPolyTree.obj")

new_faces = []
print("Faces antes: "+str(len(faces)))

for face in faces:
	if face.normals[0].z < 0:
		new_faces.append(face)
faces = new_faces
print("Faces depois: "+str(len(faces)))
lin = 150
cols = 100

COP = Vec3(0,0.5,-3)
xmin = -1
ymin = -1
xmax = 1
ymax = 2

dist = -2
width = (xmax-xmin)/cols
height = (ymax-ymin)/lin

image = np.zeros((lin, cols, 3))

for i in range(lin):
	print(i)
	for j in range(cols):
		p0 = COP
		p1 = Vec3(xmin+width*(j+0.5), ymax-height*(i+0.5), dist)
		blue, red, green  = rayTrace(p0, p1, faces)
		image[i,j, 0] = blue*255
		image[i,j, 1] = red*255
		image[i,j, 2] = green*255

print(image)
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()