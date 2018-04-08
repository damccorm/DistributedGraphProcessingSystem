"""
Worker node with purpose of computing the shortest path from a single source.
The source should initially have a value of 0 and all other vertices should
have values of -1. Each vertex will output the number of steps away it is and the
vertices on that path.
"""

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
	master = Master(ip_address)