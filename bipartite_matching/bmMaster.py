"""
Master node with purpose of computing a maximal bipartite matching.
Each vertex should initially have 1 or 2 as its value depending on which bipartite set its in.
All code created by Daniel McCormick.
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
