import json
import sys
from network import Network, Message

class Master:

	def __init__(self, own_ip = "127.0.0.1", aggregator_function = None):
		self.num_vertices = 0
		self.network = Network(own_ip, None)
		self.load_data()
		self.incoming_messages = []
		self.round_number = 0
		done = False
		aggregation_results = None
		while not done:
			self.start_round(aggregation_results)
			if self.wait_for_round():
				if aggregator_function != None:
					incoming_messages = self.get_incoming_messages()
					aggregation_results = aggregator_function(incoming_messages)
					print "Aggregation Results:", aggregation_results
			else:
				done = True
		self.network.broadcast("master", None, "DONE")
		self.output_data()

	def start_round(self, aggregation_results):
		# Start each round
		self.round_number += 1
		self.incoming_messages = []
		print "Starting round", self.round_number
		self.network.broadcast("master", str(aggregation_results), "start_round")

	def wait_for_round(self):
		# Wait for all messages to come in, store them locally in incoming_messages.
		# Return False if all vertices are inactive, True otherwise 
		num_responses = 0
		is_vertex_active = False
		while num_responses < self.num_vertices:
			received_string = self.network.wait_for_worker()
			topic, mjson = received_string.split()
			msg = json.loads(mjson)
			if topic == "worker":
				message_type = msg["message_type"]
				if message_type == "ACTIVE" or message_type == "INACTIVE":
					if message_type == "ACTIVE":
						is_vertex_active = True
					self.incoming_messages.append(Message(msg["vertex_number"], msg["contents"]))
				num_responses += 1
		return is_vertex_active

	def get_incoming_messages(self):
		return self.incoming_messages

	def output_data(self):
		# This function should be overridden. Will be run once all rounds have completed.
		print "No mechanism of outputting data provided"

	def load_data(self):
		# Receive data from loader.py, balance vertices between machines, make sure they all receive vertices, then edges.
		edge_index = 0
		while True:
			received_string = self.network.wait_for_worker()
			topic, mjson = received_string.split()
			msg = json.loads(mjson)
			if topic == "worker":
				worker_ip = msg["contents"]
				print "Adding edge to worker with ip", worker_ip
				self.network.add_edge(None, worker_ip)
			if topic == "loader":
				contents = msg["contents"]
				if contents == "DONE":
					print "Received DONE message from loader"
					return
				elif contents == "VERTEX":
					vertex_number = msg["vertex_number"]
					vertex_value = msg["vertex_value"]
					print "adding vertex", vertex_number, "with value", vertex_value
					self.network.add_vertex_to_node(vertex_number, vertex_value)
					self.num_vertices += 1
				elif contents == "EDGE":
					source = msg["source"]
					destination = msg["destination"]
					print "adding edge from", source, "to", destination
					destination_ip = self.network.vertex_number_to_ip[destination]
					self.network.send_to_worker(source, destination, destination_ip, "ADD_EDGE")
				else:
					print "ERROR, trying to load something without vertex or edge identifier"

def aggregate(incoming_messages):
	cur_max = 0
	for message in incoming_messages:
		if message.contents is not None and int(message.contents) > cur_max:
			cur_max = int(message.contents)
	return cur_max

if __name__ == '__main__':
	ip_address = "127.0.0.1"
	if len(sys.argv) > 1:
		ip_address = sys.argv[1]
	master = Master(ip_address, lambda incoming_messages: aggregate(incoming_messages))
