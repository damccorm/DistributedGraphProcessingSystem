"""
Master node with purpose of computing the shortest path from a single source.
"""
import json

def aggregate(incoming_messages):
	incoming_message_dictionaries = []
	vertex_to_set_map = {}
	min_set_number = None
	for message in incoming_messages:
		msg = json.loads(message.contents)
		incoming_message_dictionaries.append(msg)
		vertex_to_set_map[int(msg["vertex_number"])] = int(msg["set_number"])
		if min_set_number is None or min_set_number > int(msg["set_number"]):
			min_set_number = int(msg["set_number"])
	min_weight = None
	correct_vertex = None
	correct_edge = None
	if min_set_number is None:
		return None
	for msg in incoming_message_dictionaries:
		if int(msg["set_number"]) == min_set_number:
			for i in range(len(msg["edge_weights"])):
				if min_weight is None or int(msg["edge_weights"][i]) < min_weight:
					# If this edge is lower weight than the current min
					if vertex_to_set_map[int(msg["vertex_number"])] != vertex_to_set_map[int(msg["all_edges"][i])]:
						# If this edge connects 2 different sets
						min_weight = int(msg["edge_weights"][i])
						correct_vertex = msg["vertex_number"]
						correct_edge = msg["all_edges"][i]

	if correct_vertex is None:
		return None

	return str(correct_vertex) + "," + str(correct_edge) + "," + str(min_set_number)


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from master import Master
	else:
		from ..master import Master
	ip_address = "127.0.0.1"
	if len(sys.argv) > 1:
		ip_address = sys.argv[1]
	master = Master(ip_address, lambda incoming_messages: aggregate(incoming_messages))
