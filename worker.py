"""
This file contains the implementation for a worker node of a distributed graph processing system.
All code created by Daniel McCormick.
"""
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
	def __init__(self, master_ip, own_ip, compute_function, output_function = None):
		if output_function is None:
			print "No output_function provided"
		# Initialize worker, wait for master to give instructoins
		self.round_number = 0
		self.network = Network(own_ip, master_ip)
		self.network.send_to_master(None, own_ip, None)
		self.vertices = {}
		self.compute_function = compute_function
		self.output_function = output_function

		done = False
		while not done:
			done = self.listen_to_master()

	def listen_to_master(self):
		# Listen for messages from master
		received_string = self.network.wait_for_master()
		topic, mjson = received_string.split()
		msg = json.loads(mjson)

		if msg["message_type"] == "start_round":
			# Start round
			self.round_number += 1
			aggregation_results = msg["contents"]
			print "----------------------------------------------"
			print "Starting round", self.round_number, "received", aggregation_results, "from master"
			print "----------------------------------------------"
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
			if self.output_function is not None:
				print ""
				print "FINAL OUTPUT:"
				for vertex in self.vertices.values():
					print ""
					self.output_function(vertex)
			return True

		return False

	def perform_round(self, vertex, input_value):
		# Performs the round, returns appropriate result to master
		vertex, message_for_master = self.compute_function(vertex, input_value, self.round_number, self.get_incoming_messages(vertex), lambda vertex, v, value: self.send_message_to_vertex(vertex, v, value))
		active = "INACTIVE"
		if vertex.active:
			active = "ACTIVE"
		self.network.send_to_master(active, message_for_master, vertex.vertex_number)
		print "Vertex", vertex.vertex_number, "done with round, is", active, "returned value", message_for_master
		return vertex

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
		# Returns all incoming messages for that vertex sent in the previous round
		if (self.round_number-1) in vertex.incoming_messages:
			return vertex.incoming_messages[self.round_number - 1]
		return []

	def send_message_to_vertex(self, sending_vertex, receiving_vertex_number, contents):
		self.network.send_to_worker(receiving_vertex_number, sending_vertex.vertex_number, contents, self.round_number)
