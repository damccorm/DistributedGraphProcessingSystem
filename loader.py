import json
import zmq
from xlrd import open_workbook

class Loader:
	def __init__(self, master_ip, excel_file_location):
		# Reads in vertices from an excel file. 
		# Assumes vertices have the following form in sheet 1: vertex number, vertex value.
		#	The first cell should contain the number of vertices.
		# Assumes edges have the following form in sheet 2: source, destination.
		#	The first cell should contain the number of edges.
		self.context = zmq.Context()
		self.pub_socket = self.context.socket(zmq.PUB)
    	self.pub_socket.bind("tcp://"+master_ip+":5555")

		wb = open_workbook(excel_file_location)
		sheets = wb.sheets()
		vertex_sheet = sheets[0]
		edge_sheet = sheets[1]
		num_vertices = int(vertex_sheet.cell(0,0).value)
		for row in range(1, num_vertices+1):
			vertex_number = vertex_sheet.cell(row, 0).value
			vertex_value = vertex_sheet.cell(row, 1).value
			msg =  {"contents": "VERTEX",
			   		"vertex_number": vertex_number,
			   		"vertex_value": vertex_value}
        	self.master_sub_socket.send_string("%s %s" % ("loader", json.dumps(msg, separators=(",",":"))))

    	num_edges = int(edge_sheet.cell(0,0).value)
    	for row in range(1, num_edges+1):
    		source = edge_sheet.cell(row, 0).value
			destination = edge_sheet.cell(row, 1).value
			msg =  {"contents": "EDGE",
			   		"source": source,
			   		"destination": destination}
        	self.master_sub_socket.send_string("%s %s" % ("loader", json.dumps(msg, separators=(",",":"))))

        msg = {"contents": "DONE"}
		self.master_sub_socket.send_string("%s %s" % ("loader", json.dumps(msg, separators=(",",":"))))