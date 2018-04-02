from .. import worker

def compute(vertex, input_value, incoming_messages, send_message_to_vertex):
	# If largest value in existence, lock that in and stop sharing messages, otherwise, give yourself the smallest value of yourself/your neighbors
	# To be overridden
	print
	print "VERTEX", vertex.vertex_number
	value_to_aggregate = None
	if input_value is not None and int(vertex.vertex_value) == int(input_value):
		# If this vertex has the smallest input value in existence (for active vertices), mark it as inactive
		vertex.active = False
	if vertex.active:
		min_val = int(vertex.vertex_value)
		for message in incoming_messages:
			if int(message.contents) < min_val:
				min_val = int(message.contents)
		vertex.vertex_value = min_val
		for v in vertex.outgoing_edges:
			send_message_to_vertex(vertex, v, vertex.vertex_value)
		value_to_aggregate = vertex.vertex_value
	else:
		value_to_aggregate = None
	return vertex, value_to_aggregate

def output_function(vertex):
	print "Vertex", vertex.vertex_number, "finished with value", vertex.vertex_value

if __name__ == '__main__':
	master_ip_address = None
	own_ip_address = "127.0.0.2"
	if len(sys.argv) > 1:
		master_ip_address = sys.argv[1]
		if len(sys.argv) > 2:
			own_ip_address = sys.argv[2]
		compute_lambda = lambda vertex, input_value, incoming_messages, send_message_to_vertex: compute(vertex, input_value, incoming_messages, send_message_to_vertex)
		output_lambda = lambda vertex: output_function(vertex)
		worker = Worker(master_ip_address, own_ip_address, compute_lambda, output_lambda)
	else:
		print "ERROR, must add the address of the master as an argument"