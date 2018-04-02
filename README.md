This repository contains the files for a distributed graph processing system. It is based off of the Pregel Paper by Grzegorz Malewicz, Matthew H. Austern, Aart J. C. Bik, James C. Dehnert, Ilan Horn, Naty Leiser, and Grzegorz Czajkowski.

Paper here: https://kowshik.github.io/JPregel/pregel_paper.pdf

# Overview:

This system is meant to be used for distributed graph processing. It follows the model described in Pregel: there are many workers and a single master. Each vertex is placed on one of the workers. From here, the computation is divided into rounds. During each round, each vertex can do 1 of 3 things:

1) Perform computation
2) Send a message to any vertex it has an edge to
3) Receive the messages sent to it in the prior round

Each vertex also has a flag denoting whether or not it is active. At the end of each round, all vertices send their ids, whether they are active or inactive, and their values to the master. From here, the master checks if all vertices are inactive - if so, it terminates the algorithm. If not, it has the option of performing some aggregation function. It then sends the results of this aggregation function (or None if no aggregation function is provided) to the vertices, which starts the next round. Vertices can use the results of aggregation in their next round.

# Usage

## Vertex class

This project relies heavily on vertices. Each vertex has several fields:

* vertex.vertex_number - the id of the vertex
* vertex.vertex_value - the value stored at the vertex
* vertex.active - whether the vertex is active, initially True
* vertex.incoming_messages - map mapping incoming messages to the round they were sent in.
* vertex.outgoing_edges - list of outgoing edges which messages can be sent across

## Messaging class

Likewise, this project relies heavily on messaging. All messages will have 2 values - message.sending_vertex, which is the vertex_number that sent the message, and message.contents, which is the contents of the message. All contents should be sent and stored as strings.

## Files

There are 5 main files associated with this project:

* master.py
* worker.py
* loader.py
* network.py

In order to use this project, only the first 3 files are of concern

### master.py

To use the Master class from master.py, 3 arguments should be provided: the ip of the master, an aggregator function, and an output function. All communication is done through tcp, so the ip must be unique. If no aggregator function is provided, no aggregation will be done in between rounds. If one is provided, it must have the form of "lambda incoming_messages: aggregate(incoming_messages)", where incoming_messages are the messages from the vertices. Likewise, if an output function is not provided, nothing will be outputed. If one is, it should have the form of "lambda incoming_messages: aggregate(incoming_messages)", where incoming_messages are the messages from the vertices sent in the final round.

__The master must be started before any other processes.__ Once it is started, it will run until the algorithm has been terminated.

### worker.py

To use the Worker class from worker.py, 4 arguments should be provided: the ip of the master (should match the ip passed into master.py), the ip of this worker (must be unique), a compute function, and an output function. The compute function must be provided, it is recommended the output function be provided as well, though if one is not provided the workers will simply not provide output.

The compute function should have the form of "lambda vertex, input_value, incoming_messages, send_message_to_vertex: compute(vertex, input_value, incoming_messages, send_message_to_vertex)", where vertex is the Vertex object the function is manipulating, input_value is the result of the aggregation, incoming_messages is a list of messages sent to the vertex in the previous round, and send_message_to_vertex is an anonymous function that can be used to send a message along any edge, with the form send_message_to_vertex(sending_vertex, receiving_vertex_number, contents).

The output function should have the form of "lambda vertex: output_function(vertex)", where vertex is the Vertex object the function is manipulating.

### loader.py

To use the Loader class from loader.py, 2 arguments must be provided: the ip of the master (should match the ip passed into master.py) and the name of an excel .xlsx file containing the information about the graph. The excel file must be stored in the same directory as your Loader class, and should have 2 sheets with the following form:

Sheet 1 should have the number of vertices in the graph in the top left cell. Each subsequent row in the first column should contain a unique vertex id, and each corresponding row in the second column should contain a value for that vertex.

Sheet 2 should have the number of edges in the graph in the top left cell. Each subsequent row should have the source of an edge in the first column and the destination in the second column. All graphs are assumed to be directed, so to make it undirected add one edge in each direction for each edge.

# Architecture:

