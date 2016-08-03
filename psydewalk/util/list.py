def intersect(l1, l2):
	return [list(filter(lambda item: item in l1, sublist)) for sublist in l2]
