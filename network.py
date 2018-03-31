import json
import time
import zmq

class Network:
        context = zmq.Context()
        
	def __init__(self, ip_address, master_ip):
		# Socket to receive all communications not from the master
		self.not_master_sub_socket = self.context.socket(zmq.SUB)
		self.not_master_sub_socket.bind("tcp://"+ip_address+":5555")
		self.not_master_sub_socket.setsockopt_string(zmq.SUBSCRIBE, "worker".decode("ascii"))
		self.is_master = True

		#Sockets to send/receive all communications from the master
		self.master_sub_socket = None
		self.master_pub_socket = None
		if master_ip is not None:
                        self.not_master_sub_socket.RCVTIMEO = 3
			self.is_master = False
			self.master_pub_socket = self.context.socket(zmq.PUB)
			self.master_pub_socket.connect("tcp://" + master_ip + ":5555")
			self.master_sub_socket = self.context.socket(zmq.SUB)
			self.master_sub_socket.bind("tcp://"+ip_address+":5556")
			self.master_sub_socket.setsockopt_string(zmq.SUBSCRIBE, "master".decode("ascii"))
		else:
			# Make sure that master can listen for loading message as well as messages from workers
			self.not_master_sub_socket.setsockopt_string(zmq.SUBSCRIBE, "loader".decode("ascii"))

    	# List to contain sockets for all outgoing edges
		self.edges = []
		# List to contain ips for all outgoing edges. Each ip corresponds to the socket at the same index
		self.ips = []
		# Map that has vertex numbers as keys, index of outgoing sockets as values
		self.edge_map = {}
		# Map that has ip's as keys, index of outgoing sockets as values
		self.ip_map = {}
		# Map that has vertex numbers as keys, ips of nodes as keys
		self.vertex_number_to_ip = {}
		# Index of edges to add next vertex to
		self.index_of_next_vertex = 0

                # Sleep to let sockets initialize
                time.sleep(3)


        def wait_for_master(self):
		if self.is_master:
			print "ERROR, tried to wait for master from master"
			return None
		received_string = self.master_sub_socket.recv()
		return received_string

	def send_to_master(self, message_type, message_contents, vertex_number):
		if self.is_master:
			print "ERROR, tried to wait for master from master"
			return
		msg =  {"message_type": message_type, "contents": message_contents, "vertex_number": vertex_number}
		self.master_pub_socket.send_string("%s %s" % ("worker", json.dumps(msg, separators=(",",":"))))

	def add_edge(self, outgoing_vertex, outgoing_ip):
		if outgoing_ip not in self.ip_map:
			pub_socket = self.context.socket(zmq.PUB)
			if self.is_master:
				pub_socket.connect("tcp://"+outgoing_ip+":5556")
			else:
				pub_socket.connect("tcp://"+outgoing_ip+":5555")
			self.edges.append(pub_socket)
			self.ips.append(outgoing_ip)
			self.ip_map[outgoing_ip] = len(self.edges) - 1
		if outgoing_vertex is not None and outgoing_vertex not in self.edge_map:
			self.edge_map[outgoing_vertex] = self.ip_map[outgoing_ip]

	def send_to_worker(self, receiving_vertex, sending_vertex, message_contents, message_type):
		msg =  {"message_type": message_type,
				"contents": message_contents,
				"sending_vertex": sending_vertex,
				"destination_vertex": receiving_vertex}
		cur_socket = self.edges[self.edge_map[receiving_vertex]]
		sender = "worker"
		if self.is_master:
			sender = "master"
		cur_socket.send_string("%s %s" % (sender, json.dumps(msg, separators=(",",":"))))

	def wait_for_worker(self):
		received_string = self.not_master_sub_socket.recv()
		return received_string

	def broadcast(self, sending_vertex, message_contents, message_type):
		for vertex in self.edge_map.keys():
			self.send_to_worker(vertex, sending_vertex, message_contents, message_type)

	def add_vertex_to_node(self, vertex_number, vertex_value):
                print self.index_of_next_vertex, self.edges
		msg =  {"message_type": "ADD_VERTEX",
				"vertex_number": vertex_number,
				"vertex_value": vertex_value}
		cur_socket = self.edges[self.index_of_next_vertex]
		self.vertex_number_to_ip[vertex_number] = self.ips[self.index_of_next_vertex]
		cur_socket.send_string("%s %s" % ("master", json.dumps(msg, separators=(",",":"))))
                self.edge_map[vertex_number] = self.index_of_next_vertex
		self.index_of_next_vertex = (self.index_of_next_vertex+1) % len(self.edges)
