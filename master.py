import json
from network import Network

class Master:

	def __init__(self, own_ip = "127.0.0.1"):
		self.num_vertices = 0
		self.network = Network(own_ip, None)
		self.load_data(msg)
		self.incoming_messages = []
		done = False
		aggregation_results = None
		while not done:
			self.start_round(aggregation_results)
			if self.wait_for_round():
				aggregation_results = self.aggregate()
			else:
				done = True
		self.output_data()

	def start_round(self, aggregation_results):
		# Start each round
		self.incoming_messages = []
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
					self.incoming_messages.append(msg)
		return is_vertex_active

	def get_incoming_messages(self):
		return self.incoming_messages

	def aggregate(self):
		# This function should be overridden. 
		# Will be run at end of every round except for last to aggregate data.
		print "No aggregation function provided"
		return

	def output_data(self):
		# This function should be overridden. Will be run once all rounds have completed.
		print "No mechanism of outputting data provided"

	def load_data(self, msg):
		# Receive data from loader.py, balance vertices between machines, make sure they all receive vertices, then edges.
		edge_index = 0
		while True:
			received_string = self.network.wait_for_worker()
			topic, mjson = received_string.split()
			msg = json.loads(mjson)
			if topic == "worker":
				worker_ip = msg["contents"]
				self.network.add_edge(None, worker_ip)
			if topic == "loader":
				contents = msg["contents"]
				if contents == "DONE":
					return
				elif contents == "VERTEX":
					print "adding vertex"
					vertex_number = msg["vertex_number"]
					vertex_value = msg["vertex_value"]
					self.network.add_vertex_to_node(vertex_number, vertex_value)
					self.num_vertices += 1
				elif contents == "EDGE":
					print "adding edge"
					source = msg["source"]
					destination = msg["destination"]
					self.network.send_to_worker(source, "master", destination, "ADD_EDGE")
				else:
					print "ERROR, trying to load something without vertex or edge identifier"
