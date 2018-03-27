import json
import sys
from network import Network

class Message:
	def __init__(self, sending_vertex, contents):
		self.sending_vertex = sending_vertex
		self.contents = contents

class Vertex:
	def __init__(self, vertex_number, vertex_value):
		self.vertex_number = vertex_number
		self.vertex_value = vertex_value
		self.active = True
		# Maps round number messages were received as key to list of messages as value
		self.incoming_messages = {}

class Worker:
	def __init__(self, master_ip = "127.0.0.1", own_ip = "127.0.0.2"):
		self.round_number = 0
		self.network = Network(own_ip, master_ip)
		self.network.send_to_master(None, own_ip, None)
		self.vertices = {}
		while True:
			received_string = self.network.wait_for_master()
			topic, mjson = received_string.split()
			msg = json.loads(mjson)
			if msg["message_type"] == "start_round":
				self.round_number += 1
				aggregation_results = msg["contents"]
				for vertex_number in self.vertices:
					vertex = self.vertices[vertex_number]
					self.vertices[vertex_number] = self.perform_round(vertex, input_value)
			elif msg["message_type"] == "ADD_VERTEX":
				self.vertices[msg["vertex_number"]] = Vertex(int(msg["vertex_number"]), msg["vertex_value"])
			elif msg["message_type"] == "ADD_EDGE":
				vertex = msg["destination_vertex"]
				outgoing_ip = msg["contents"]
				self.network.add_edge(vertex, outgoing_ip)

	def perform_round(self, vertex, input_value):
		self.receive_incoming_messages()
		vertex, message_for_master = self.compute(vertex, input_value)
		active = "INACTIVE"
		if vertex.active:
			active = "ACTIVE"
		self.network.send_to_master(active, message_for_master, vertex.vertex_number)
		return vertex

	def receive_incoming_messages(self):
		while True:
			# TODO: Add timeout to make sure this doesn't loop forever.
			received_string = self.network.wait_for_worker()
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

	def get_incoming_messages(vertex):
		return vertex.incoming_messages[self.round_number]

	def compute(self, vertex, input_value):
		# To be overridden
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