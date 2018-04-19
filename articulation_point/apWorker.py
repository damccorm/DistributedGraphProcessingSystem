"""
Master node with purpose of finding an articulation point.
Each vertex should initially have 0 as it's value.
Assumes an undirected graph.
"""

import json

def compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex):
	# Approach - do a DFS with every node as the root of at least one tree. Any tree with 2+ children is an articulation point.
	# To do DFS, each message will contain the root and a list of visited vertices.
	if round_number == 1:
		# Assume its not an articulation point until proven otherwise
		vertex.vertex_value = False
		msg = {"root": vertex.vertex_number, "dfs": [vertex.vertex_number]}
		if len(vertex.outgoing_edges) > 1:
			send_message_to_vertex(vertex, vertex.outgoing_edges[0], json.dumps(msg, separators=(",",":")))
		else:
			vertex.active = False
	elif len(incoming_messages) > 0:
		vertex.active = True
		for message in incoming_messages:
			msg = json.loads(message.contents)
                        print msg
			if msg["root"] == vertex.vertex_number:
				# Don't forward, just check if it has 2 children in tree
                                vertex.active = False
				for i in range(1, len(vertex.outgoing_edges)):
					if vertex.outgoing_edges[i] not in msg["dfs"]:
						vertex.vertex_value = True
			else:
				# Continue to go in dfs
				sent_on = False
				if vertex.vertex_number not in msg["dfs"]:
					msg["dfs"].append(vertex.vertex_number)
				for v in vertex.outgoing_edges:
					if not sent_on and v not in msg["dfs"]:
						send_message_to_vertex(vertex, v, json.dumps(msg, separators=(",",":")))
                                                print v, "TEST1"
						sent_on = True
				if not sent_on:
					# Climb back on up tree
					cur_dfs_num = msg["dfs"].index(vertex.vertex_number)
					parent_found = False
					cur_index = cur_dfs_num - 1
					while cur_index >= 0 and not parent_found:
						for v in vertex.outgoing_edges:
							if int(msg["dfs"][cur_index]) == int(v):
						if int(msg["dfs"][parent_index]) in vertex.outgoing_edges and parent_index == -1:
							send_message_to_vertex(vertex, v, json.dumps(msg, separators=(",",":")))
							parent_found = True
                            print v, "TEST2"
	else:
	        print vertex.vertex_value
	return vertex, None

def output_function(vertex):
	if vertex.vertex_value:
		print "Vertex", vertex.vertex_number, "is an articulation point"
	else:
		print "Vertex", vertex.vertex_number, "is not an articulation point"

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
