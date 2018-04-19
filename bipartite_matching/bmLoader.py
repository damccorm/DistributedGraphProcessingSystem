"""
Loader node with purpose of computing a maximal bipartite matching.
Each vertex should initially have 1 or 2 as its value depending on which bipartite set its in.
All code created by Daniel McCormick.
"""

if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from loader import Loader
	else:
		from ..loader import Loader
	excel_filename = "bmGraph.xlsx"
	if len(sys.argv) > 1:
		master_ip_address = sys.argv[1]
		loader = Loader(master_ip_address, excel_filename)
	else:
		print "ERROR, must add the address of the master as an argument"
