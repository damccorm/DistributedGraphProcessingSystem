"""
Worker node with purpose of computing the minimum spanning tree.
Each vertex should initially have the comma seperated weights of its edges (sorted by 
vertex number) as it's value. So if a vertex has an edge of weight 3 to vertex 1 and an
edge of weight 2 to vertex 3, it's value will initially be 3,2
"""

import json

def compute(vertex, input_value, incoming_messages, send_message_to_vertex):
	if not isinstance(vertex.vertex_value, dict):
		# If not list, must be the first round
		edge_weights = [int(float(x)) for x in str(vertex.vertex_value).split(",")]
		# Sort outgoing edges so they match weights.
		# We'll just do bubble sort, not optimal obviously
		for i in range(len(vertex.outgoing_edges)):
			for j in range(len(vertex.outgoing_edges) - 1):
				if int(vertex.outgoing_edges[j]) > int(vertex.outgoing_edges[j+1]):
					vertex.outgoing_edges[j], vertex.outgoing_edges[j+1] = vertex.outgoing_edges[j+1], vertex.outgoing_edges[j]

		vertex.vertex_value =  {"edge_weights": edge_weights, 
								"added_edges": [], 
								"all_edges": vertex.outgoing_edges, 
								"set_number": vertex.vertex_number, 
								"vertex_number": vertex.vertex_number}
	else:
		if input_value is None or input_value == "None":
			vertex.active = False
		else:
			correct_vertex, correct_edge, set_number = [int(float(x)) for x in input_value.split(",")]
			to_be_added = None
			if correct_vertex == vertex.vertex_number:
				to_be_added = correct_edge
				vertex.active = False
			elif correct_edge == vertex.vertex_number:
				to_be_added = correct_vertex
				vertex.vertex_value["set_number"] = set_number
				# Now part of MST, so can be marked inactive safely.
				vertex.active = False
			if to_be_added is not None:
				vertex.vertex_value["added_edges"].append(to_be_added)

	# Send aggregator info, it will choose smallest edge from smallest set
	return vertex, json.dumps(vertex.vertex_value, separators=(",",":"))

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
