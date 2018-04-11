"""
Worker node with purpose of computing the 2 coloring.
Each vertex should initially have 0 as its value
"""

import json

def compute(vertex, input_value, incoming_messages, send_message_to_vertex):
	if input_value is not None:
		print "TODO - original color selection here"
		# No messages sent last time
		if int(input_value) == vertex.vertex_number:
			vertex.vertex_value = 1
			for v in vertex.outgoing_edges:
				send_message_to_vertex(vertex, v, vertex.vertex_value)
			return vertex, vertex.vertex_value
	elif vertex.vertex_value is None or int(vertex.vertex_value) > 0:
		# Value has already been set
		return vertex, None
	else:
		if len(incoming_messages) > 0:
			vertex.active = False
			adjacent_color = incoming_messages[0].contents
			for message in incoming_messages:
				if message.contents != adjacent_color:
					adjacent_color = None
					break
			if adjacent_color is None:
				vertex.vertex_value = None
			elif int(adjacent_color) == 1:
				vertex.vertex_value = 2
			else:
				vertex.vertex_value = 1

			if vertex.vertex_value is None:
				return vertex, 0
			else:
				for v in vertex.outgoing_edges:
					send_message_to_vertex(vertex, v, vertex.vertex_value)
				return vertex, vertex.vertex_value
				

def output_function(vertex):
	# TODO
	print "Vertex", vertex.vertex_number, "has edges to the following vertices:", vertex.vertex_value["added_edges"]


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
