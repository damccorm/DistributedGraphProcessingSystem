"""
Loader node with purpose of computing the max flow.
Each vertex should initially have the comma seperated weights of its edges (sorted by 
vertex number) as it's value. So if a vertex has an edge of weight 3 to vertex 1 and an
edge of weight 2 to vertex 3, it's value will initially be 3,2.
If the vertex is the source, it should have a value of -1 appended to the end of this, if
it is the destination it should have a value of -2 appended to the end of this.
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
	excel_filename = "mfGraph.xlsx"
	if len(sys.argv) > 1:
		master_ip_address = sys.argv[1]
		loader = Loader(master_ip_address, excel_filename)
	else:
		print "ERROR, must add the address of the master as an argument"
