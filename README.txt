README

This coding challenge is solved with three main files:
The first file is main - where input and output targets are entered using the -i 
flag to enter an input file path and the -o flag as the output file path
	e.g. python ./src/main.py -i ./venmo_input/venmo-trans.txt -o ./venmo_output/output.txt

The second file is parser which reads in each line and converts the json format to a usable
tuple dictionary in python. This class checks to make sure no empty actors or targets are added to the graph. 

The last file is graph which takes the python tuple and creates graphs and edges based on the timestamp, actor and target in the tuple. This class checks for duplicate targets or actors and if they are duplicate nodes then the correct node will be fetched. It also checks for duplicate edges between the same actor and target or vice versa. In this case, the code will update the timestamp, but not generate a duplicate edge. The list of edges is also sorted every time an edge is added. This reduces the time complexity, as it is unnecessary to iterate through the entire list of edges, but only the edges that are expired. Once an edge is reached that has not expired, as the list is sorted, the function is exited because all remaining timestamps will be within the window.
