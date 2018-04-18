"""
Master node with purpose of computing the max flow.
Each vertex should initially have the comma seperated weights of its edges (sorted by 
vertex number) as it's value. So if a vertex has an edge of weight 3 to vertex 1 and an
edge of weight 2 to vertex 3, it's value will initially be 3,2.
If the vertex is the source, it should have a value of -1 appended to the end of this, if
it is the destination it should have a value of -2 appended to the end of this.
"""
import json

def aggregate(incoming_messages):

	for message in incoming_messages:
		if message.contents is not None and message.contents != "None":
			return message.contents


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
