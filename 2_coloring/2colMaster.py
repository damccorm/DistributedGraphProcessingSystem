"""
Master node with purpose of computing the 2 coloring.
Each vertex should initially have 0 as its value
"""
def aggregate(incoming_messages):
	cur_return_val = None
	for message in incoming_messages:
                print message.contents
		if message.contents is not None and message.contents != "None":
			if int(message.contents) == 0:
				cur_return_val = message.sending_vertex
			else:
				return None
        return cur_return_val

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
