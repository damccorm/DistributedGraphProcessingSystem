"""
Worker node with purpose of computing a maximal independent set.
Each vertex should initially have 0 as its value.
"""

def compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex):
	if vertex.active:
		if round_number%3 == 1:
			for v in vertex.outgoing_edges:
				send_message_to_vertex(vertex, v, vertex.vertex_number)
		elif round_number%3 == 2:
			for m in incoming_messages:
				if int(m.sending_vertex) < vertex.vertex_number:
					return vertex, None
			vertex.vertex_value = 1
			vertex.active = False
			for v in vertex.outgoing_edges:
				send_message_to_vertex(vertex, v, vertex.vertex_number)
		else:
			if len(incoming_messages) > 0:
				# Neighbor must have been added to IS
				vertex.active = False
	return vertex, None
				

def output_function(vertex):
	if vertex.vertex_value == 1:
		print "Vertex", vertex.vertex_number, "is part of the independent set"
	else:
		print "Vertex", vertex.vertex_number, "is not part of the independent set"


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
		compute_lambda = lambda vertex, input_value, round_number, incoming_messages, send_message_to_vertex: compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex)
		output_lambda = lambda vertex: output_function(vertex)
		worker = Worker(master_ip_address, own_ip_address, compute_lambda, output_lambda)
	else:
		print "ERROR, must add the address of the master as an argument"
