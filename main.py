import cv2
import numpy as np

import loadObj
from loadObj import *
		

luzAmbiente = [1,1,1]
m = 10
def rayTrace(p0, p1, faces, COP):

	#vetor u
	raio = Vec3(p1.x-p0.x, p1.y-p0.y, p1.z-p0.z)

	normal_prox = None
	menor_z = None
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
				if(menor_z == None):
					menor_z = p_plano.z
					normal_prox = normal_plano
				elif p_plano.z < menor_z:
					normal_prox = normal_plano

	if normal_prox == None:
		return 0,0,0

	ka_reflex = [0, 0.8, 0.0]
	kd_reflex = [0, 0.8, 0.0]
	ks_reflex = [0, 0.8, 0.0]

	vetDifusa = Vec3(3,1,0)

	nvl = np.power(2*vectorialProd(normal_prox, vetDifusa)*vectorialProd(normal_prox, COP)-vectorialProd(COP, vetDifusa), m)
	normal_luz = vectorialProd(normal_prox, vetDifusa)
	blue = ka_reflex[0]*luzAmbiente[0]*normal_luz+ka_reflex[0]*luzAmbiente[0]*nvl
	green = ka_reflex[1]*luzAmbiente[1]*normal_luz+ka_reflex[1]*luzAmbiente[1]*nvl
	red = ka_reflex[2]*luzAmbiente[2]*normal_luz+ka_reflex[2]*luzAmbiente[2]*nvl

	return blue, green, red 			

def preencheLinha(i, lin, cols, COP, xmin, ymin, xmax, ymax, image, dist, width, height):
	print(i)
	for j in range(cols):
		p0 = COP
		p1 = Vec3(xmin+width*(j+0.5), ymax-height*(i+0.5), dist)
		blue, green, red  = rayTrace(p0, p1, faces, COP)
		image[i,j, 0] = blue*255
		image[i,j, 1] = green*255
		image[i,j, 2] = red*255

print("Hello World")

vertices, normals, faces = loadObj.readObj("LowPolyTree.obj")

new_faces = []
print("Faces antes: "+str(len(faces)))

for face in faces:
	if face.normals[0].z < 0:
		new_faces.append(face)
faces = new_faces
print("Faces depois: "+str(len(faces)))
lin = 360
cols = 240

COP = Vec3(0,0,-3)
xmin = -1
ymin = -1
xmax = 1
ymax = 2

dist = -1
width = (xmax-xmin)/cols
height = (ymax-ymin)/lin

image = np.zeros((lin, cols, 3))

for i in range(lin):
	preencheLinha(i, lin, cols, COP, xmin, ymin, xmax, ymax, image, dist, width, height)

print(image)
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()