import json
import sys
import zmq
from network import Network, Message
class Vertex:
	# Class that contains all the info about an individual vertex
	def __init__(self, vertex_number, vertex_value):
		self.vertex_number = vertex_number
		self.vertex_value = vertex_value
		self.active = True
		# Maps round number messages were received as key to list of messages as value
		self.incoming_messages = {}
		# Outgoing edges contains the vertices this vertex has edges to.
		self.outgoing_edges = []

class Worker:
	def __init__(self, master_ip = "127.0.0.1", own_ip = "127.0.0.2"):
		# Initialize worker, wait for master to give instructoins
		self.round_number = 0
		self.network = Network(own_ip, master_ip)
		self.network.send_to_master(None, own_ip, None)
		self.vertices = {}

		while True:
			self.listen_to_master()
			

	def listen_to_master(self):
		# Listen for messages from master
		received_string = self.network.wait_for_master()
		topic, mjson = received_string.split()
		msg = json.loads(mjson)

		if msg["message_type"] == "start_round":
			# Start round
			self.round_number += 1
			print "Starting round", self.round_number
			aggregation_results = msg["contents"]
			if aggregation_results is not None and aggregation_results == "None":
				aggregation_results = None
			self.receive_incoming_messages()
			for vertex_number in self.vertices:
				vertex = self.vertices[vertex_number]
				self.vertices[vertex_number] = self.perform_round(vertex, aggregation_results)

		elif msg["message_type"] == "ADD_VERTEX":
			# Add a vertex to this machine
			self.vertices[msg["vertex_number"]] = Vertex(int(msg["vertex_number"]), msg["vertex_value"])
			print "Added vertex", msg["vertex_number"], "with value", msg["vertex_value"]

		elif msg["message_type"] == "ADD_EDGE":
			# Add an edge from a vertex on this machine to another vertex
			source = msg["destination_vertex"]
			destination = msg["sending_vertex"]
			outgoing_ip = msg["contents"]
			self.network.add_edge(destination, outgoing_ip)
			self.vertices[source].outgoing_edges.append(destination)
			print "Added edge from", source, "to", destination

		elif msg["message_type"] == "DONE":
			self.output_results()

	def perform_round(self, vertex, input_value):
		# Performs the round, returns appropriate result to master
		vertex, message_for_master = self.compute(vertex, input_value)
		active = "INACTIVE"
		if vertex.active:
			active = "ACTIVE"
		self.network.send_to_master(active, message_for_master, vertex.vertex_number)
		print "Vertex", vertex.vertex_number, "done with round, is", active, "returned value", message_for_master
		return vertex

	def output_results():
		# Output results at end of algorithm
		print "Results go here"


	def receive_incoming_messages(self):
		# Receives all incoming messages from workers, parses them into Message objects, and sorts them to the appropriate vertex.
		while True:
			try:
				received_string = self.network.wait_for_worker()
			except:
				return
			topic, mjson = received_string.split()
			msg = json.loads(mjson)
			round_number_sent_in = msg["message_type"]
			sender = msg["sending_vertex"]
			receiver = msg["destination_vertex"]
			contents = msg["contents"]
			message = Message(sender, contents)
			vertex = self.vertices[receiver]
			if int(round_number_sent_in) in vertex.incoming_messages:
				vertex.incoming_messages[int(round_number_sent_in)].append(message)
			else:
				vertex.incoming_messages[int(round_number_sent_in)] = [message]

	def get_incoming_messages(self, vertex):
		# Returns all incoming messages for that vertex for the round
                if self.round_number in vertex.incoming_messages:
		        return vertex.incoming_messages[self.round_number]
                return []

	def send_message_to_vertex(self, sending_vertex, receiving_vertex_number, contents):
		self.network.send_to_worker(receiving_vertex_number, sending_vertex.vertex_number, contents, self.round_number)

	def compute(self, vertex, input_value):
		# If largest value in existence, lock that in and stop sharing messages, otherwise, give yourself the smallest value of yourself/your neighbors
		# To be overridden
		print "Master input value", input_value
                print "Vertex", vertex.vertex_number, "has edges", vertex.outgoing_edges
		value_to_aggregate = None
		if input_value is not None and int(vertex.vertex_value) == int(input_value):
			# If this vertex has the smallest input value in existence (for active vertices), mark it as inactive
			vertex.active = False
		if vertex.active:
			incoming_messages = self.get_incoming_messages(vertex)
			min_val = int(vertex.vertex_value)
			for message in incoming_messages:
                                print "Received value", message.contents
				if int(message.contents) < min_val:
					min_val = int(message.contents)
			vertex.vertex_value = min_val
			for v in vertex.outgoing_edges:
				self.send_message_to_vertex(vertex, v, vertex.vertex_value)
                                print "Sent message to vertex", v
                        value_to_aggregate = vertex.vertex_value
		else:
			value_to_aggregate = None
		return vertex, value_to_aggregate

if __name__ == '__main__':
	master_ip_address = None
	own_ip_address = "127.0.0.2"
	if len(sys.argv) > 1:
		master_ip_address = sys.argv[1]
		if len(sys.argv) > 2:
			own_ip_address = sys.argv[2]
		worker = Worker(master_ip_address, own_ip_address)
	else:
		print "ERROR, must add the address of the master as an argument"
