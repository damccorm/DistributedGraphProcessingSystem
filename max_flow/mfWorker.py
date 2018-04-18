"""
Worker node with purpose of computing the max flow.
Each vertex should initially have the comma seperated weights of its edges (sorted by 
vertex number) as it's value. So if a vertex has an edge of weight 3 to vertex 1 and an
edge of weight 2 to vertex 3, it's value will initially be 3,2.
If the vertex is the source, it should have a value of -1 appended to the end of this, if
it is the destination it should have a value of -2 appended to the end of this.
"""

import json

def compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex):
	if round_number == 1:
		edge_weights = [int(float(x)) for x in str(vertex.vertex_value).split(",")]
		# Sort outgoing edges so they match weights.
		# We'll just do bubble sort, not optimal obviously
		for i in range(len(vertex.outgoing_edges)):
			for j in range(len(vertex.outgoing_edges) - 1):
				if int(vertex.outgoing_edges[j]) > int(vertex.outgoing_edges[j+1]):
					vertex.outgoing_edges[j], vertex.outgoing_edges[j+1] = vertex.outgoing_edges[j+1], vertex.outgoing_edges[j]

		edge_flows = []
		for i in edge_weights:
			edge_flows.append(0)

		is_source = (len(edge_weights) > len(vertex.outgoing_edges) and edge_weights[-1] == -1)
		is_destination = (len(edge_weights) > len(vertex.outgoing_edges) and edge_weights[-1] == -2)
		vertex.vertex_value =  {"edge_capacities": edge_weights, 
								"edge_flows": edge_flows,
								"source": is_source,
								"destination": is_destination}

	if input_value is not None:
		# Path has been found, assume return aggregator sends message as serialized dict with following form:
		# {path: set of all vertices on path, flow: max flow that can be sent on path}
		msg = json.loads(input_value)
		path = msg["path"]
		if vertex.vertex_number in path:
			flow = int(msg["flow"])
			for i in range(len(vertex.outgoing_edges)):
				if vertex.outgoing_edges[i] in path and vertex.vertex_value["edge_capacities"][i] > 0:
					# This is the correct edge in the path
					vertex.vertex_value["edge_capacities"][i] -= flow
					vertex.vertex_value["edge_flows"][i] += flow
		vertex.active = True

	if input_value is not None or round_number == 1:
		# Start searching for new path because we are just starting or we just found a path
		if vertex.vertex_value["source"]:
			# Start search
			for i in range(len(vertex.outgoing_edges)):
				if vertex.vertex_value["edge_capacities"][i] > 0:
					msg_to_send = {"path": {vertex.vertex_number: True}, "flow": vertex.vertex_value["edge_capacities"][i]}
					send_message_to_vertex(vertex, vertex.outgoing_edges[i], json.dumps(msg_to_send, separators=(",",":")))
	elif len(incoming_messages) > 0:
		vertex.active = True
		# Try to add self to path
		msg = json.loads(incoming_messages[0].contents)
		msg["path"][vertex.vertex_number] = True
		flow = msg["flow"]
		if vertex.vertex_value["destination"]:
			# If destination, send path to master along with flow
			return vertex, json.dumps(msg, separators=(",",":"))
		else:
			# Otherwise, pass it on
			for i in range(len(vertex.outgoing_edges)):
				if vertex.vertex_value["edge_capacities"][i] > 0:
					if vertex.vertex_value["edge_capacities"][i] < flow:
						msg["flow"] = vertex.vertex_value["edge_capacities"][i]
					send_message_to_vertex(vertex, vertex.outgoing_edges[i], json.dumps(msg, separators=(",",":")))
					msg["flow"] = flow
	else:
		# Didn't receive any messages, mark self inactive
		vertex.active = False

	# Send aggregator info, it will choose smallest edge from smallest set
	return vertex, None

def output_function(vertex):
	# TODO
	print "Vertex", vertex.vertex_number, "has the following value:", vertex.vertex_value


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
