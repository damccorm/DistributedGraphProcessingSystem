"""
Worker node with purpose of computing the pagerank.
Each vertex should initially have the number of vertices in the graph as its value.
All code created by Daniel McCormick.
"""


def compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex):
        vertex.vertex_value
	if round_number == 1:
		num_vertices_in_graph = float(vertex.vertex_value)
		vertex.vertex_value = [1.0, num_vertices_in_graph]
	else:
		cur_sum = 0.0
		for message in incoming_messages:
			cur_sum += float(message.contents)
		vertex.vertex_value[0] = (0.15/vertex.vertex_value[1]) + (0.85*cur_sum)
        output_val = vertex.vertex_value[0]/float(len(vertex.outgoing_edges))
        for v in vertex.outgoing_edges:
                send_message_to_vertex(vertex, v, output_val)
	if round_number == 50:
		vertex.active = False
	return vertex, None
				

def output_function(vertex):
	print "Vertex", vertex.vertex_number, "has a PageRank of", vertex.vertex_value[0]


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
