from src.utilities.ilp_manager import *
from src.utilities.cdfg_manager import *
import matplotlib.pyplot as plt
import re
import logging

# function to do sqrt in trivial way
def sqrt(n):
	i = 0
	while (i*i) < n:
		i+=1
	return i

############################################################################################################################################
############################################################################################################################################
#
#	`SCHEDULER` CLASS
#
############################################################################################################################################
#	DESCRIPTION:
#					The following class is used as a scheduler a CDFG (Control DataFlow Graph) representing a function. 
#					It elaborates the CDFG of an IR (Intermediare Representation).
#					Then, it generates its scheduling depending on the scheduling technique selected
############################################################################################################################################
#	ATTRIBUTES:
#					- parser : parser used to generate CDFG after parsing SSA IR
#					- cdfg : CDFG representation of the SSA IR input
#					- cfg : CFG representation of the SSA IR input
#					- sched_tech : scheduling technique selected
#					- sched_sol : scheduling solution
#					- ilp: ilp object
#					- constraints: constraints object
#					- obj_fun: optmization function object
#					- II : Initiation Interval achieved by scheduling solution
#					- log: logger object used to output logs
############################################################################################################################################
#	FUNCTIONS:
#					- set_sched_technique : set scheduling technique
#					- add_artificial_nodes : create super nodes
#					- set_data_dependency_constraints: setting the data dependency constraints
#					- set_max_latency_constraints: setting the initialization interval to the value II_value
#					- add_sink_delays_constraints : add sink delays constraints
#					- set_obj_function: setting the optimiztion function, according to the optimization option
#					- create_scheduling_ilp : create the ILP of the scheduling
#					- solve_scheduling_ilp: solve the ilp and obtain scheduling
#					- get_sink_delays: get delays of sinks after computing solution
#					- print_gantt_chart : prints the gantt chart of a scheduling solution
#					- print_scheduling_summary: it prints the start time of each node into a txt report. If the loop is pipelined, it also prints the achieved II.
############################################################################################################################################
############################################################################################################################################


scheduling_techniques = ["asap", "alap", "pipelined"]

class Scheduler:

	# initialization of the scheduler with the parser
	def __init__(self, parser, sched_technique, log=None):
		if log != None:
			self.log = log
		else:
			self.log = logging.getLogger('scheduler') # if the logger is not given at object generation, create a new one
		self.parser = parser
		self.cdfg = parser.get_cdfg()
		self.cfg = parser.get_cfg()
		self.add_artificial_nodes() # adding supersource and supersinks to the cdfg
		self.set_sched_technique(sched_technique)
		self.sched_sol = None
		self.II = None

		# set solver options
		self.ilp = ILP(log=log)
		self.constraints = Constraint_Set(self.ilp, log=log)
		self.obj_fun = Obj_Function(self.ilp, log=log)

		# define ilp variable per each node
		self.add_nodes_to_ilp()
		pass
	
	"""
	Adds supersinks and supernodes to the CDFG and connects them to the existing nodes according the the conventions in the assignment
	"""
	def add_artificial_nodes(self):
		for bb in self.cfg:
			numericBBID = bb.attr["id"]
			bbLabel = bb.attr["label"]

			supersource_name = f"ssrc_{numericBBID}"
			supersink_name = f"ssink_{numericBBID}"

			self.cdfg.add_node(supersource_name, id=numericBBID, bbID=bbLabel, type="supersource", label=
			supersource_name)
			self.cdfg.add_node(supersink_name, id=numericBBID, bbID=bbLabel, type="supersink", label=
			supersink_name)

			for node in self.cdfg:
				if node.attr.get("id") != numericBBID: # Not in current BB
					continue		
				if node.attr.get("type") in ["supersource", "supersink"]: # Not artificial
					continue

				back_edge = True
				for pred in self.cdfg.in_neighbors(node): # Check non-back edge nodes
					if pred.attr.get("id") != numericBBID: 
						continue

					edge = self.cdfg.get_edge(pred, node)

					if edge.attr.get("style", "solid") != "dashed":
						back_edge = False
						break

				if back_edge: # Add edge to supernode if no Non-Back Edge
					self.cdfg.add_edge(supersource_name, node)
				
				back_edge = True
				for succ in self.cdfg.out_neighbors(node): # Check non-back edge nodes
					if succ.attr.get("id") != numericBBID:
						continue

					edge = self.cdfg.get_edge(node, succ)

					if edge.attr.get("style", "solid") != "dashed":
						back_edge = False
						break

				if back_edge: # Add edge to supernode if no Non-Back Edge
					self.cdfg.add_edge(node, supersink_name)

		#draw the cdfg for testing your code in task 1
		self.cdfg.layout(prog='dot')
		self.cdfg.draw('output.pdf')

	"""
	Adds the scheduling variable of each node in the CDFG to the ILP formulation.
	"""
	def add_nodes_to_ilp(self):
		for node in self.cdfg:
			if node.attr.get("type") == "supersource":
				self.ilp.add_variable(f"sv{node}", lower_bound=0, var_type="i")
			else:
				self.ilp.add_variable(f"sv{node}", var_type="i")

	"""
	Adds data dependency constraints to the scheduler object's constraint set based on the edges between CDFG nodes.
	"""
	def set_data_dependency_constraints(self):
		for node in self.cdfg:
			for succ in self.cdfg.out_neighbors(node):

				if node.attr.get("id") != succ.attr.get("id"): # Not in current BB
					continue 
				
				edge = self.cdfg.get_edge(node, succ)

				if edge.attr.get("style", "solid") == "dashed": # Not Back Edge
					continue 

				lhs_dictionary = {}
				lhs_dictionary[f"sv{succ}"] = 1   
				lhs_dictionary[f"sv{node}"] = -1    

				rhs = get_node_latency(node.attr)

				self.constraints.add_constraint(lhs_dictionary, "geq", rhs)

	"""
	Adds the constraints needed to allow minimizing the ASAP objective function to produce a valid result.
	"""
	def create_asap_scheduling_ilp(self):
		self.set_data_dependency_constraints()

	"""
	Adds terms to the objective function with coefficients that will ensure each node is scheduled ASAP.
	"""
	def set_asap_objective_function(self):
		for node in self.cdfg:
			self.obj_fun.add_variable(f"sv{node}", 1)

	"""
	Returns the sv of each BB's supersink in the form of a dictionary/list
	"""
	def get_sink_svs(self):
		sink_svs ={}
		for node in self.cdfg:
			if node.attr.get("type") == "supersink":
				sink_svs[f"{node}"] = self.ilp.get_operation_timing_solution(node)
		return sink_svs

	"""
	Sets maximum sv constraints for each BB according to values passed to in in a dictionary, intended for ALAP
	@type sink_svs: dictionary
	@param sink_svs: a dictionary containing an identifier for a BB and a corresponding maximum sv
	"""
	def add_sink_sv_constraints(self, sink_svs):
		for sink_label, sink_delays in sink_svs.items():
			lhs_dictionary = {}
			lhs_dictionary[f"sv{sink_label}"] = 1
			self.constraints.add_constraint(lhs_dictionary, "leq", sink_delays)

	"""
	Adds the constraints needed to allow minimizing the ALAP objective function to produce a valid result.
	"""
	def create_alap_scheduling_ilp(self, sink_svs):
		self.set_data_dependency_constraints()
		self.add_sink_sv_constraints(sink_svs)

	"""
	Adds terms to the objective function with coefficients that will ensure each node is scheduled ALAP.
	"""
	def set_alap_objective_function(self):
		for node in self.cdfg:
			self.obj_fun.add_variable(f"sv{node}", -1)

	"""
	Adds constraints that enforce inter-iteration data dependencies
	@type II: integer
	@param II: the II value for writing the inter-iteration data dependencies.
	"""
	def set_pipelining_constraints(self, II):
		for node in self.cdfg:
			for succ in self.cdfg.out_neighbors(node):

				edge = self.cdfg.get_edge(node, succ)
				if edge.attr.get("style", "solid") != "dashed": # Only consider Back Edge
					continue  			

				lhs_dictionary = {}
				lhs_dictionary[f"sv{succ}"] = 1
				lhs_dictionary[f"sv{node}"] = -1
				
				rhs = get_node_latency(node.attr) - II
				
				self.constraints.add_constraint(lhs_dictionary, "geq", rhs)

	"""
	Adds the constraints needed to allow minimizing the ALAP objective function to produce a valid result.
	"""
	def create_pipelined_scheduling_ilp(self, II):
		self.set_data_dependency_constraints()
		self.set_pipelining_constraints(II)

	"""
	Returns the numeric id of the BB to be pipelined
	"""
	def find_loop_bb(self):
		max_latency = -1
		loop_bb = None

		for bb in self.cdfg:
			supersink_latency = None

			for node in self.cdfg:
				if node.attr.get("id") == bb.attr.get("id") and node.attr.get("type") == "supersink":
					supersink_latency = self.ilp.get_operation_timing_solution(node)
					break

			if supersink_latency is not None and supersink_latency > max_latency:
				max_latency = supersink_latency
				loop_bb = bb

		return loop_bb



#### DO NOT TOUCH FROM THIS LINE ####

	def pass_scheduling_ilp(self, resources):
		resources.set_scheduling_ilp(self.ilp, self.constraints, self.obj_fun)

	"""
	Sets the scheduling technique of the scheduler
	@type technique: String
	@param technique: The name of the scheduling technique
	"""
	def set_sched_technique(self, technique):
		assert(technique in scheduling_techniques) # the scheduling technique chosen must belong to the allowed ones
		self.log.info(f'Setting the scheduling technique to be "{technique}"')
		self.sched_tech = technique

	"""
	Create the complete ILP scheduling by calling functions that add constraints and create the optimization function according to the scheduling technique
	@type sink_sv: dictionary
	@param sink_svs: dictionary containing BB latency bounds for ALAP
	"""
	def create_scheduling_ilp(self, sink_svs=None, II=None):
		if self.sched_tech == "asap":
			self.create_asap_scheduling_ilp()
		elif self.sched_tech == "alap":
			self.create_alap_scheduling_ilp(sink_svs)
		elif self.sched_tech == "pipelined":
			self.create_pipelined_scheduling_ilp(II)
			self.II = II

		self.set_obj_function()

	"""
	Create the optimization function by adding variables to the obj_fun object according to the specified scheduling technique
	"""
	def set_obj_function(self):
		if self.sched_tech == 'asap':
			self.set_asap_objective_function()
		elif self.sched_tech == 'alap':
			self.set_alap_objective_function()
		elif self.sched_tech == 'pipelined':
			self.set_asap_objective_function()
		else:
			self.log.error(f'Not implemented option! {self.sched_tech}')
			raise NotImplementedError
		

	# function to solve the ilp and obtain scheduling
	def solve_scheduling_ilp(self, base_path, example_name):
		# log the result
		self.ilp.print_ilp("{0}/{1}/output.lp".format(base_path, example_name))
		res = self.ilp.solve_ilp()
		if res != 1:
			self.log.warn("The ILP problem cannot be solved")
			return res
		self.sched_sol = self.ilp.get_ilp_solution() # save solution in an attribute
		# iterate through the different variables to obtain results
		for var, value in self.ilp.get_ilp_solution().items():
			node_type = 'AUX'
			# check if the node represents a timing
			if re.search(r'^sv', var):
				node_name = re.sub(r'^sv', '', var)
				attributes = self.cdfg.get_node(node_name).attr
				node_type = attributes['type']
				attributes['label'] = attributes['label'] + '\n' + f'[{value}]'
				attributes['latency'] = value
			self.log.debug(f'{var} of type {node_type}:= {value}')
		self.cdfg.draw("test_dag_result.pdf", prog="dot")
		if 'max_latency' in self.ilp.get_ilp_solution():
			self.log.info(f'The maximum latency for this cdfg is {self.ilp.get_ilp_solution()["max_latency"]}')
		elif 'max_II' in self.ilp.get_ilp_solution():
			self.log.info(f'The maximum II for this cdfg is {self.ilp.get_ilp_solution()["max_II"]}')
			self.II = self.ilp.get_ilp_solution()["max_II"]
		elif self.II is not None:
			self.log.info(f'The II for this cdfg is {self.II}')
		return res

	# function to get the gantt chart of a scheduling
	def print_gantt_chart(self, chart_title="Untitled", file_path=None):
		assert self.sched_sol != None, "There should be a solution to an ILP before running this function"
		variables = {}
		start_time = {}
		duration = {}
		latest_tick = {} # variable to find last tick for xlables
		bars_colors = {}
		for node_name in get_cdfg_nodes(self.cdfg):
			if 'label' in self.cdfg.get_node(node_name).attr:
				attributes = self.cdfg.get_node(node_name).attr
				bb_id = attributes['id']
				if not(bb_id in variables):
					variables[bb_id] = []
					start_time[bb_id] = []
					duration[bb_id] = []
					bars_colors[bb_id] = []
					latest_tick[bb_id] = 0
				#type should also be printed
				graph_name = node_name + " Type: " + attributes['type']
				variables[bb_id].append(graph_name)
				start_time[bb_id].append(float(attributes['latency'])) # start time of each operation
				node_latency = float(get_node_latency(attributes))
				if attributes["type"] == "zext":
					bars_colors[bb_id].append("yellowgreen")
				elif attributes["type"] == "add":
					bars_colors[bb_id].append("plum")
				elif attributes["type"] == "mul":
					bars_colors[bb_id].append("orange")
				else:
					if node_latency == 0.0:
						node_latency = 0.1
						bars_colors[bb_id].append("firebrick")
					else:
						bars_colors[bb_id].append("dodgerblue")
				
				
				duration[bb_id].append(node_latency) # duration of each operation
				tmp_tick = float(attributes['latency']) + float(get_node_latency(attributes))
				if tmp_tick > latest_tick[bb_id]:
					latest_tick[bb_id] = tmp_tick
		graphs_per_row = sqrt(len(variables))
		#fig, axs = plt.subplots(int(len(variables)))
		fig = plt.figure(figsize=(20 * 1.5, 11.25 * 1.5), constrained_layout=True)
		axs=[]
		subplot_format = (graphs_per_row * 110) + 1

		axs_id = 0
		for bb_id in variables:
			axs.append(fig.add_subplot(subplot_format))
			subplot_format += 1
			axs[axs_id].barh(y=variables[bb_id], left=start_time[bb_id], width=duration[bb_id], color=bars_colors[bb_id])
			axs[axs_id].grid()
			axs[axs_id].set_xticks([i for i in range(int(latest_tick[bb_id])+1)])
			axs[axs_id].title.set_text("BB {}".format(bb_id))
#			if self.II != None: # adding II information on the plot
#				axs[axs_id].hlines(y=-1, xmin=0, xmax=self.II, color='r', linestyle = '-')
#				axs[axs_id].text(self.II/2-0.35, -2, "II = {0}".format(int(self.II)), color='r')
			axs_id += 1
		#plt.title(chart_title)
		fig.canvas.manager.set_window_title(chart_title)
		if file_path != None:
			plt.savefig(file_path)
		# plt.show()

	
		if "pipe" in self.sched_tech:

			variables = []
			start_time = []
			duration = []
			latest_tick = 0  # variable to find last tick for xlables
			bars_colors = []

			bbnum = 0


			#kernel 3 and 4's loop are both in BB1
			nodes = [n for n in get_cdfg_nodes(self.cdfg) if n.attr['id'] == str(self.find_loop_bb())]
			for it in range(1,-1, -1):
				for node in nodes:
					if 'label' in self.cdfg.get_node(node).attr:
						attributes = self.cdfg.get_node(node).attr
						bb_id = attributes['id']
						# if not(bb_id in variables):
						# 	print("sad")
						# 	print(node)
						# 	variables = []
						# 	start_time = []
						# 	duration = []
						# 	bars_colors = []
						# 	latest_tick = 0
						#type should also be printed

						graph_name = node + " Type: " + attributes['type'] + " Iter: " + str(it)
						variables.append(graph_name)
						start_time.append(float(attributes['latency']) + self.II*it) # start time of each operation

						# variables[bb_id].append(graph_name + " Iteration 2")
						# start_time[bb_id].append(float(attributes['latency']) + self.sched_sol["II"]) # also append the second iteration
						node_latency = float(get_node_latency(attributes))
						#append twice
						if attributes["type"] == "zext":
							bars_colors.append("yellowgreen")
						elif attributes["type"] == "add":
							bars_colors.append("plum")
						elif attributes["type"] == "mul":
							bars_colors.append("orange")
						else:
							if node_latency == 0.0:
								node_latency = 0.1
								bars_colors.append("firebrick")
							else:
								bars_colors.append("dodgerblue")
						duration.append(node_latency) # duration of each operation
						tmp_tick = (float(attributes['latency']) + self.II*it)
						# print(f"graph name {graph_name} it {it} tmp_tick {tmp_tick} latest_tick {latest_tick}")
						if tmp_tick > latest_tick:
							latest_tick = tmp_tick
			graphs_per_row = sqrt(len(variables))
			#fig, axs = plt.subplots(int(len(variables)))
			fig = plt.figure(figsize=(20 * 1.5, 11.25 * 1.5))
			axs=[]
			subplot_format = (graphs_per_row * 110) + 1
			# print(str(graphs_per_row) + "graph per row")
			axs_id = 0

			# print(subplot_format)
			axs.append(fig.add_subplot())
			subplot_format += 1
			axs[axs_id].barh(y=variables, left=start_time, width=duration, color=bars_colors)
			axs[axs_id].grid()
			axs[axs_id].set_xticks([i for i in range(int(latest_tick)+1)])
			axs[axs_id].title.set_text("BB {}".format(bb_id))
#			if self.II != None: # adding II information on the plot
#				axs[axs_id].hlines(y=-1, xmin=0, xmax=self.II, color='r', linestyle = '-')
#				axs[axs_id].text(self.II/2-0.35, -2, "II = {0}".format(int(self.II)), color='r')
			axs_id += 1
			#plt.title(chart_title)
			fig.canvas.manager.set_window_title(chart_title)
			if file_path != None:
				split = file_path.split(".")
				# print(split[0])
				file_path = split[0] + "_loop_iter.pdf"
				plt.savefig(file_path)
			# plt.show()


	# function to get the gantt chart of a scheduling solution
	def print_scheduling_summary(self, file_path=None):
		assert self.sched_sol != None, "There should be a solution to an ILP before running this function"
		with open(file_path, 'w') as f:
			# sort the summary by BBs, print the starting time of each node
			for id_ in range(len(self.cfg)):
				# sort the summary by starting time of each node
				for node in sorted(get_cdfg_nodes(self.cdfg), key=lambda n : n.attr["latency"]):
					if int(node.attr['id']) == id_:
						f.write(f'sv({node}) @ bb({id_}) := {node.attr["latency"]}\n')
			if self.II != None:
				f.write(f'II := {self.II}')
			else:
				f.write(f'II := N/A')
