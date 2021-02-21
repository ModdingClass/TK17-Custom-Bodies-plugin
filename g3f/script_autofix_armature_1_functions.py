def getCenter(vertex_index_list, obj):
	print (obj.name)
	vertex_list = [obj.data.vertices[i] for i in vertex_index_list]
	count = float(len(vertex_list))
	x, y, z = [ sum( [v.co[i] for v in vertex_list] ) for i in range(3)]
	center = (Vector( (x, y, z ) ) / count ) 
	return center
