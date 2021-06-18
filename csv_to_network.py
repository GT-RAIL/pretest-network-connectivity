import random

# goes through every node to find the lowest hop count (nothing fancy, just BFS)
def determineOptimalHops(network):
    lowest_hop_count = float("inf")

    # for each node in the graph
    for start_node in network:
        flipped = [str(start_node)]
        frontier = [str(start_node)]
        hops = 0
        # while the frontier isn't empty
        while len(frontier) > 0:
            new_frontier = []  # reset the frontier
            for node in frontier:  # for each node in the old frontier
                for connection in network[node]["connections"]:  # for each connection to each frontier node
                    if str(connection) not in flipped and str(connection) not in new_frontier:  # if the connection is not already flipped color, add it to the new frontier
                        new_frontier.append(str(connection))
                flipped.append(str(node))  # flip this node
            frontier = [x for x in new_frontier]  # set the new frontier
            hops += 1  # increment hops
        if hops < lowest_hop_count:  # if this node has less hops than the lowest hop count, update the lowest hop count
            lowest_hop_count = hops
    return lowest_hop_count

output = ""

# for each network, make the function
for network_name in ["Baseline", "Large", "Semilong", "Shortcut", "Small", "Sparse", "Tree", "TreeShortcut", "TreeShuffle"]:

    print("Generating network " + network_name)

    network = {}

    # pull the network out of the network name file
    with open("Kilshin/" + network_name + ".csv", "r") as f:
        lines = f.readlines()

        # for each line after the first line (header)
        for line in lines[1:]:
            # split the line into a list of stats
            node_stats = line.split(",")

            # parse the stats
            node_id = node_stats[0]
            node_x = node_stats[1]
            node_y = node_stats[2]
            connections = [int(x.replace("\"", "").replace(" ", "").replace("[", "").replace("]", "").replace("\n", "")) for x in node_stats[3:]]

            # put the node into the network
            network[node_id] = {"x": node_x, "y": node_y, "connections": connections}

    # generate the JavaScript function output

    # header
    output += "// [autogenerated] Kilshin network - " + network_name
    output += "\nfunction generatePuzzleKilshin" + network_name + "() {"

    # node locations
    output += "\n    // first record the location of each node, as an x% y% of the canvas"
    for node in network:
        output += "\n    var node_" + node + "_loc = [" + network[node]["x"] + ", " + network[node]["y"] + "];"
    output += "\n"

    # node objects
    output += "\n    // second create the node objects"
    for node in network:
        output += "\n    var node_" + node + " = new Node(gameboard.context, node_" + node + "_loc);"
    output += "\n"

    # node connections
    output += "\n    // third connect the nodes, running a connection from A->B will also create the connection from B->A"
    connections = []  # store the connections to prevent duplicates (A->B, B->A), although it won't matter, just to reduce lines
    for node in network:
        for connected_node_id in network[node]["connections"]: 
            if sorted([int(node), connected_node_id]) not in connections:
                output += "\n    node_" + node + ".connect(node_" + str(connected_node_id) + ");"
                connections.append(sorted([int(node), connected_node_id]))
    output += "\n"

    # nodes to network
    output += "\n    // fourth add the nodes to the network"
    output += "\n    networks.nodes = [" + ", ".join(["node_" + x for x in network]) + "];"
    output += "\n"

    # game parameters
    output += "\n    //  fifth set the game parameters"
    output += "\n    networks.observationNodes = " + str(random.sample(range(0, len(list(network.keys()))), 3)) + ";"
    output += "\n    networks.optimalHops = " + str(determineOptimalHops(network)) + ";"
    output += "\n    networks.maxRounds = 3;"
    output += "\n}"

    # double newline at end
    output += "\n\n\n"

with open("Kilshin/KilshinPuzzles.js", "w") as f:
    f.write(output)

print("Completed generating network, output in Kilshin/KilshinPuzzles.js")


        
