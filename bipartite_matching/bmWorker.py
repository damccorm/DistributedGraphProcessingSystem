"""
Worker node with purpose of computing a maximal bipartite matching.
Each vertex should initially have 1 or 2 as its value depending on which bipartite set its in.
"""
import random

def compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex):

	if round_number == 1:
		vertex.vertex_value = [int(vertex.vertex_value), None]
	if vertex.vertex_value[1] is not None:
		# You've already been matched
		return vertex, None

	if round_number%2 == 1:
		if vertex.vertex_value[0] == 1:
			if len(incoming_messages) > 0:
				# You've been matched
				vertex.vertex_value[1] = incoming_messages[0].contents
				vertex.active = False
			else:
				edge_index = (round_number-1)/2
				if edge_index >= len(vertex.outgoing_edges):
					# We've tried all edges, give up
					vertex.active = False
				else:
					v = vertex.outgoing_edges[edge_index]
					send_message_to_vertex(vertex, v, vertex.vertex_number)
	else:
		if vertex.vertex_value[0] == 2:
			# We'll just let the vertices in the first set control when the algorithm terminates
			vertex.active = False
			if len(incoming_messages) > 0:
				matched_message = random.choice(incoming_messages)
				vertex.vertex_value[1] = matched_message.contents
				send_message_to_vertex(vertex, int(vertex.vertex_value[1]), int(vertex.vertex_value[1]))
        return vertex, None
				

def output_function(vertex):
	# TODO
	print "Vertex", vertex.vertex_number, "has been matched with", vertex.vertex_value[1]


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
