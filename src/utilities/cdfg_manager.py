############################################################################################################################################
############################################################################################################################################
#
#	CDFG MANAGER
#
############################################################################################################################################
#	FUNCTIONS:
#				- get_node_latency : retrieve a synthetic latency from the attribute of the cdfg node
#				- get_cdfg_edges : retrieve edges of cdfg
#				- get_cdfg_nodes : retrieve nodes of cdfg
#				- update_dic_list : update the value of a key (where the value is a list)
#				- create_control_edge : create a control edge between src and dst in the cdfg
#				- is_control_edge : check if edge between src and dst is a control edge
#				- get_topological_order : assume that the input graph is a DAG, return the topological order of the nodes
############################################################################################################################################
############################################################################################################################################


# function to retrieve the delay from the type
def get_node_latency(attr):
	if attr['type'] == 'mul' or attr['type'] == 'div':
		return 4
	elif attr['type'] == 'load':
		return 1
	elif attr['type'] in ('br', 'supersink', 'supersource', 'constant'):
		return 0
	else:
		return 1

# function to retrieve edges of cdfg
def get_cdfg_edges(cdfg):
	return sorted(map(lambda e : cdfg.get_edge(*e), cdfg.edges(keys=True)), reverse=True)

# function to retrieve nodes of cdfg
def get_cdfg_nodes(cdfg):
	return sorted(map(lambda n : cdfg.get_node(n), cdfg.nodes()), reverse=True)

# function to retrieve all dag edges of cdfg
def get_dag_edges(cdfg):
	is_dag_edges = lambda e : e.attr['style'] != 'dashed'
	return filter(is_dag_edges, get_cdfg_edges(cdfg))

# function to retrieve all the back edges that are not in the DAG
def get_back_edges(cdfg):
	is_bak_edges = lambda e : e.attr['style'] == 'dashed'
	return filter(is_bak_edges, get_cdfg_edges(cdfg))


# function to update the value of a key (where the value is a list)
def update_dic_list(dic, key, new_element):
	if key in dic:
		inst_list = dic[key]
	else:
		inst_list = []
	inst_list.append(new_element)
	dic[key] = inst_list
	return dic

# function to create a control edge between src and dst in the cdfg
def create_control_edge(cdfg, src, dst):
	cdfg.add_edge(src, dst, style="dashed")
	return cdfg

# function to check if edge between src and dst is a control edge
def is_control_edge(cdfg, src, dst):
	pass


''' assume that the input graph is a DAG, return topological ordering among the nodes
	https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search '''

def get_topological_order(cdfg):
	node_list = get_topological_order_kahn(cdfg)
	return node_list

def get_topological_order_kahn(cdfg):
	nodes = get_cdfg_nodes(cdfg)

	in_degree = { node: 0 for node in nodes}

	dag_edges = list(get_dag_edges(cdfg))
    
	for edge in dag_edges:
		source, target = edge[0], edge[1]
		in_degree[target] += 1       

	queue = [node for node, deg in in_degree.items() if deg == 0]
    
	topo_order = []
    
    # Process nodes in the queue.
	while queue:
		current = queue.pop(0)
		topo_order.append(current)
        
        # Look for outgoing DAG edges from 'current' and reduce the in-degree of their targets.
		for edge in dag_edges:
			if edge[0] == current:
				target = edge[1]
				in_degree[target] -= 1
                # If in-degree becomes zero, add the target to the queue.
				if in_degree[target] == 0:
					queue.append(target)
    
    # Check if a topological ordering is found for all nodes.
	if len(topo_order) != len(nodes):
		raise Exception("Cycle detected (ignoring dashed edges) - topological sort not possible.")
    
	return topo_order

def get_topological_order_dfs(cdfg):
	# node_list: historical ordering
	# temp_list: a DFS run
	node_list, temp_list = [], []
	def visit(node):
		if node in node_list:
			return
		assert node not in temp_list, 'error - the CDFG graph should not contain not dashed loop back edges!'
		temp_list.append(node)
		for e in get_cdfg_edges(cdfg):
			# skip to visit the dashed edges: they are for sure cyclic
			if e[0] == node and not ('style' in e.attr and e.attr['style'] == 'dashed'): 
				visit(e[1])
		node_list.insert(0, node)
		temp_list.remove(node)
	
	# we call a separate DFS per each node
	for node in get_cdfg_nodes(cdfg): 
		if node not in node_list:
			visit(node)
	
	return node_list


	
