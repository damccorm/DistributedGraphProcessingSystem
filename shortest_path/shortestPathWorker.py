# NOTE: This doesn't do what it should yet.

def compute(vertex, input_value, incoming_messages, send_message_to_vertex):
	# If largest value in existence, lock that in and stop sharing messages, otherwise, give yourself the smallest value of yourself/your neighbors
	# To be overridden
	return vertex, 0

def output_function(vertex):
	print "Vertex", vertex.vertex_number, "finished with value", vertex.vertex_value


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
