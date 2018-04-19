"""
Worker node with purpose of computing a 2x approximation vertex cover.
Each vertex should initially have 0 as its value.
All code created by Daniel McCormick.
"""

def compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex):
	if round_number == 1:
		return vertex, vertex.vertex_number
	if vertex.active:=
		if round_number % 3 == 1 and vertex.vertex_value == -1:
			vertex.active = False
			if len(incoming_messages) > 0:
				vertex.vertex_value = 1
				send_message_to_vertex(vertex, int(incoming_messages[0].sending_vertex), "ADD")
		elif round_number%3 == 2:
			if len(incoming_messages) > 0:
				vertex.vertex_value = 1
				vertex.active = False
			elif input_value is None:
				vertex.active = False
			elif int(input_value) == vertex.vertex_number:
				for v in vertex.outgoing_edges:
					send_message_to_vertex(vertex, v, "MAYBE_ADD")
				vertex.vertex_value = -1
		else:
			if len(incoming_messages) > 0:
				send_message_to_vertex(vertex, int(incoming_messages[0].sending_vertex), "MAYBE_ADD")
	else:
		return vertex, None
	return vertex, vertex.vertex_number
				

def output_function(vertex):
	if vertex.vertex_value == 1:
	        print "Vertex", vertex.vertex_number, "is part of the cover"
        else:
                print "Vertex", vertex.vertex_number, "is not part of the cover"


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
