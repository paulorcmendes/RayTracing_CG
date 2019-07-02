class Vec3(object):
	"""docstring for Vec3"""
	def __init__(self, x, y, z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
	
	def toString(self):
		return "x: "+str(self.x)+" y: "+str(self.y)+" z: "+str(self.z)

class Face(object):

	def __init__(self, vertices, normals):
		self.vertices = vertices
		self.normals = normals

	def toString(self):
		msg = ""
		for i in range(len(self.vertices)):
			msg += str(i)+": V "+self.vertices[i].toString()+" N "+self.normals[i].toString()+"\n"
		return msg

def readObj(file_name):
	faces = []
	with open(file_name) as file:
		lines = file.read().split('\n')	
		#print(lines)
		vertices = []
		normals = []	

		for line in lines:
			content = line.split(' ')
			#print(content)

			if(content[0] == "v"):
				vertices.append(Vec3(content[1], content[2], content[3]))

			elif (content[0] == "vn"):
				normals.append(Vec3(content[1], content[2], content[3]))
			elif(content[0] == "f"):
				f_vertices = []
				f_normals = []
				for i in range(1,4):
					elements = content[i].split("/")
					v_index = int(elements[0])-1
					n_index = int(elements[2])-1
					f_vertices.append(vertices[v_index])
					f_normals.append(normals[n_index])
				faces.append(Face(f_vertices, f_normals))
		for face in faces:
			print(face.toString())
	return faces