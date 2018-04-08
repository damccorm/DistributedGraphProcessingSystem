"""
Worker node with purpose of computing the shortest path from a single source.
The source should initially have a value of 0 and all other vertices should
have values of -1. Each vertex will output the number of steps away it is and the
vertices on that path.
"""

def compute(vertex, input_value, incoming_messages, send_message_to_vertex):
        print incoming_messages
        vertex.active = False
	if type(vertex.vertex_value) is not list:
		# If not list, must be the first round
		if vertex.vertex_value == -1:
			vertex.vertex_value = []
		else:
                        vertex.active = True
			vertex.vertex_value = [vertex.vertex_number]
			for v in vertex.outgoing_edges:
				send_message_to_vertex(vertex, v, vertex.vertex_value)
	elif len(incoming_messages) > 0:
		for message in incoming_messages:
			if len(vertex.vertex_value) == 0 or len(message.contents) + 1 < len(vertex.vertex_value):
				# If this is new shortest path, set it as such, broadcast that.
				# Stay active so synchronizer doesn't terminate algorithm.
				vertex.vertex_value = message.contents
				vertex.vertex_value.append(vertex.vertex_number)
				vertex.active = True
                                for v in vertex.outgoing_edges:
				        send_message_to_vertex(vertex, v, vertex.vertex_value)
	else:
		vertex.active = False		
	return vertex, None

def output_function(vertex):
	print "Vertex", vertex.vertex_number, "is", len(vertex.vertex_value)-1, "steps away from the source"
	print "The path from source to vertex", vertex.vertex_number, "is", vertex.vertex_value


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from worker import Worker
	else:
		from ..worker import Worker
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
