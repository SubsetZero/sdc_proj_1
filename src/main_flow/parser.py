import re
import pygraphviz as pgv
import logging
from llvmlite.binding import parse_assembly, get_function_cfg

if __name__ == '__main__':
	print("ERROR - Use option --frontend with the run_SDC.py script to run only the parser")
	exit()

# this imports are relative to SDC main path, so they shouldn't be run if the script run on its own
from src.utilities.regex import *
from src.utilities.cdfg_manager import *


############################################################################################################################################
############################################################################################################################################
#
#	`PARSER` CLASS
#
############################################################################################################################################
#	DESCRIPTION:
#					The following class is used as a parser of an IR (Intermediate Representation) of LLVM (https://llvm.org/).
# 					It elaborates the IR to generate a CDFG (Control DataFlow Graph) representation of the input function.
#					Then, the CDFG is used in the following steps of the SDC project
############################################################################################################################################
#	ATTRIBUTES:
#					- ssa_path : path location of the input SSA IR
#					- example_name : name of the input function
#					- assembly : text of the input SSA IR
#					- top_function : name of the top function
#					- function_inputs : inputs of the top function
#					- cfg : output CFG of the parser
#					- dic_bbID : dictionary of bb_IDNumber per bbID
#					- cdfg : output CDFG of the parser
#					- dic_nodes : dictionary of nodes per type
#					- log: logger object used to output logs
############################################################################################################################################
#	FUNCTIONS:
#					- is_valid : check validity of the parser object
#					- read_ssa_file : read the SSA IR input file
# 					- set_top_function : set top_function name
#					- create_cfg : create control flow graph of the SSA IR input file
#					- is_backedge : check if the edge is a back edge
#					- create_cdfg : create CDFG output
#					- parse_cdfg_instruction : parse instruction from SSA IR to create CDFG nodes and edges
#					- create_bb_control_signals : create a control wire between BBs (connecting branch(es) and phi(s) )
#					- draw_cdfg : represent CDFG in an output file
#					- get_cdfg : get CDFG output
#					- get_cfg : get CFG output
############################################################################################################################################
############################################################################################################################################

class Parser():

	# it takes as input the ssa_path where the SSA IR is located and the name of the input function
	def __init__(self, ssa_path, example_name, log=None):
		if log != None:
			self.log = log
		else:
			self.log = logging.getLogger('parser') # if the logger is not given at object generation, create a new one
		self.ssa_path = ssa_path
		self.example_name = example_name

		self.read_ssa_file(ssa_path) #function to set the parser assembly
		self.set_top_function(example_name) #it assumes that the filename corresponds to top function
		self.create_cfg() # it generates the control flow graph
		self.create_cdfg() # it generates the control data flow graph

	#function to check validity of the parser
	def is_valid(self):
		valid = True
		if self.ssa_path == None or not(".ll" in self.ssa_path):
			self.log.error("SSA path is wrong ({0}). Please check the correct path and the correct format (.ll)".format(self.ssa_path))
			valid = False
		if self.assembly == None:
			self.log.error("Assembly is invalid. You need to call read_ssa_file function at least once")
			valid = False
		if self.top_function == None:
			self.log.error("Top_function is invalid. You need to call set_top_function function at least once")
			valid = False
		return valid

	#function to read ssa file and check its validity
	def read_ssa_file(self, ssa_path):

		with open(ssa_path, 'r') as f:
			ssa = f.read()
		self.assembly = parse_assembly(ssa)
		self.assembly.verify()

	#function to set top function of the input assembly file
	def set_top_function(self, top_function_name):
		assert(not(self.assembly is None)) #check that assembly is not None and the read_ssa_file has been called at least once
		for function in self.assembly.functions:
			if re.search(top_function_name, function.name):
				self.top_function = function
				# finding and setting inputs of function
				for line in str(function).split("\n"):
					if "define" in line and top_function_name in line:
						input_regex = r'\(((, )?(\S+)\*? %(\S+))*\)'
						match_input = re.search(input_regex, line)
						if not match_input: self.log.error(f'line that failed to match: {line}')
						matched_string = match_input.group()
						splitted_matched_string = matched_string.split()
						self.function_inputs = []
						for i in range(len(splitted_matched_string)):
							if i % 2 != 0:
								self.function_inputs.append(splitted_matched_string[i].replace(",","").replace(")","").replace("%","_"))

	# function to create control flow graph of the assembly code
	def create_cfg(self):
		# generating dictionary containing the bbID as keys and bb_IDNum as value ( for example bbID is 'entry' and bb_IDNum is 0)
		self.dic_bbID = dict([ (bb_node.name, bb_IDNum) for bb_IDNum, bb_node in enumerate(self.top_function.blocks) ])
		init_cfg = pgv.AGraph(get_function_cfg(self.top_function, False)) # obtaining initial cfg from pygraphviz
		# dictionary with bb_node instance as keys and bb_label as values
		dic_bbNode_bbLabel = dict([ (bb_node, re.search(r'\{([\w.]+)', bb_node.attr['label']).group(1)) for bb_node in get_cdfg_nodes(init_cfg) ])
		self.cfg = pgv.AGraph() # empty graph
		for bbNode in get_cdfg_nodes(init_cfg):
			label = dic_bbNode_bbLabel[bbNode] # label of bb_node instance
			idNum = self.dic_bbID[label] # id number of bb_node instance
			self.cfg.add_node(label, id=idNum, label=f'BB{idNum}\n({label})') # adding node in CFG
		for bb_edge in get_cdfg_edges(init_cfg): # add each BB edge in the CFG
			bb_src = bb_edge[0]
			bb_dst = bb_edge[1]
			self.cfg.add_edge(dic_bbNode_bbLabel[bb_src], dic_bbNode_bbLabel[bb_dst])

	# function to check if the edge is backedge
	def is_backedge(self, src, dst):
		src_bbID, dst_bbID = self.cdfg.get_node(src).attr['bbID'], self.cdfg.get_node(dst).attr['bbID'] # retrieve src and dst bbID
		is_src_not_cst = src.attr['type'] != 'constant' # the src shouldn't be a constant
		is_dst_phi = dst.attr['type'] == 'phi' # the dst should be a 'phi' type node
		bbID_cons_order = self.dic_bbID[src_bbID] >= self.dic_bbID[dst_bbID] # the BB id of the src should be the same or later one than the one of dst
		return is_src_not_cst and is_dst_phi and bbID_cons_order

	#function to create the cdfg representation of the assembly code
	def create_cdfg(self):
		assert(not(self.top_function is None)) #check that top_function it not None and the set_top_function has been called at least once
		self.cdfg = pgv.AGraph(strict=False, directed=True)
		self.dic_nodes = {} # dictionary of nodes per type # format = { "type1" = [a, b, c], ...} where type1 is a node type and a,b,c are labels
		for basic_block in self.top_function.blocks: #iterate trough basic blocks to generate the cdfg with instructions as nodes
			for instruction in basic_block.instructions:
				self.parse_cdfg_instruction(str(instruction), self.cdfg, str(basic_block.name)) # each instruction is instantiated inside the cdfg

		# get entry BB information
		entry_bb_label, entry_bb_num = [ (bb_name, bb_num) for bb_name, bb_num in self.dic_bbID.items() if bb_num == 0 ][0]
		# associate entry BB to each function argument
		for arg in get_cdfg_nodes(self.cdfg):
			if arg.attr['type'] == 'argument':
				arg.attr['bbID'] = entry_bb_label
				arg.attr['id'] = entry_bb_num

		for bb_id in set([ node.attr['bbID'] for node in get_cdfg_nodes(self.cdfg) if node.attr['bbID'] != '' ]): # iterating through the BB ids to recreate BB graph
			self.cdfg.add_subgraph([ str(cdfg_node) for cdfg_node in get_cdfg_nodes(self.cdfg) if cdfg_node.attr['bbID'] == bb_id ], name = f'cluster_{bb_id}', color = 'darkgreen', label = bb_id)
			# associating to each node in the cdfg the corresponding BB id it belongs to

		# creating the bb control signals between branch(es) and phi(s)
		self.create_bb_control_signals()

	# function to parse each instruction
	def parse_cdfg_instruction(self, instruction, cdfg, bbID):
		assert type(instruction) == str # the instruction input type should be string
		operands, result, label = [], '', instruction
		# iterating through all regex instruction to indentify a candidate instruction
		for instruction_key, instruction_regex in all_regex_instructions.items():
			match = re.search(instruction_regex, instruction)
			if match:
				# depending on the type of instruction different information extraction are applied
				# the match groups depend on the regex (see utilities.regex.py for detailed list of regex)
				# binary intruction case
				bitwidth = 0 # by default, we assign bitwidth = 0 for all operations
				# we associate bitwidth of the variable to the operation that produces it
				if instruction_key in binary_instructions: # instruction format: result = binary_instruction output_type input_1 input_2
					operands = [ n for n in match.groups() if n != None][-2:]
					result = match.group(1)
					if instruction_key == 'icmp':
						bitwidth = 1 # comparators have boolean output
						label = 'icmp_' + match.group(2) + ' ' + result # icmp instruction format: result = icmp icmp_type output_type input_1 input_2
					else:
						label = instruction_key + ' ' + result
						bitwidth = re.match(r'(f|i)(\d+)', match.groups()[-3])[2]
				# unary instruction case
				elif instruction_key in unary_instructions:
					if "ext" in instruction_key: # instruction format: result = unary_instruction input_type input to output_type
						operands = [match.group(3)]
						result = match.group(1)
						label = instruction_key + ' ' + result
						bitwidth = re.match(r'(f|i)(\d+)', match.groups()[-1])[2]
					elif instruction_key == "fneg": # fneg instruction format: result = fneg output_type input
						operands = [ n for n in match.groups() if n != None][-1]
						result = match.group(1)
						label = instruction_key + ' ' + result
						bitwidth = re.match(r'(f|i)(\d+)', match.groups()[-1])[2]
				# memory instruction case
				elif instruction_key in memory_instructions:
					if "load" in instruction_key:
						operands = [ match.group(5) ]
						result = match.group(1)
						label = 'load_' + result
						bitwidth = re.match(r'(f|i)(\d+)', match.groups()[2])[2]
					elif instruction_key == 'store':
						operands = match.group(3, 5)
						result = 'store_' + match.group(5)
						label = 'store_' + result
						bitwidth = re.match(r'(f|i)(\d+)', match.groups()[1])[2]
					elif instruction_key == 'getelementptr':
						operands = match.group(4, 6)
						result = match.group(1)
						label = instruction_key + ' ' + result
						bitwidth = re.match(r'(f|i)(\d+)', match.groups()[1])[2]
				# control instruction case
				elif instruction_key in control_instructions:
					if instruction_key == 'ret':
						operands = [match.group(2)]
						result = f'ret_{bbID}'
						label = result
					elif instruction_key == 'br':
						operands = [match.group(1)]
						result = f'br_{bbID}'
						label = result
					elif instruction_key == 'phi':
						result = match.group(1)
						label = instruction_key + ' ' + result
						input_regex = r'\[(\s)*(\S+)(\s)*,(\s)*(\S+)(\s)*\]' # input format: [value, label]
						for n in match.groups()[-2:]:
							if n != None:
								match_input = re.search(input_regex,n)
								if match_input != None:
									operands.append(match_input.group(2))
						bitwidth = re.match(r'(f|i)(\d+)', match.groups()[9])[2]
				else:
					self.log.error("Identifying instruction '{0}'".format(instruction))

				self.log.debug(f'The bitwidth of label {label} is {bitwidth}')

				# update the dictionary containing the list of nodes per type
				self.dic_nodes = update_dic_list(self.dic_nodes ,instruction_key, result.replace('%', '_'))
				break

		result = result.replace('%', '_')
		constants = [ op for op in operands if '%' not in op ] # constants are operands without initial '%' symbol
		variables = [ op.replace('%', '_') for op in operands if '%' in op ] # variables are operands with initial '%' symbol
		if result != '':
			cdfg.add_node(f'{result}', label = label.replace('%', '_'), id = self.dic_bbID[bbID], bbID = bbID, instruction = instruction.strip(), type=instruction_key, bitwidth=bitwidth) # add node related to the instruction
			self.log.debug("Added node {0} with input variable {1} and input constant {2}".format(label, variables, constants))
			for input_ in variables: # add a node for each input variable if not present and the edge connecting it to result
				if input_ in self.function_inputs:
					# if the variable is a function input, the bbid is assigned depending on last operation calling it, and we call the type of this variable "argument"
					#cdfg.add_node(f'{input_}', id = self.dic_bbID[bbID], bbID = bbID, type='argument')
					cdfg.add_node(f'{input_}', type='argument')
				else:
					cdfg.add_node(f'{input_}')
				cdfg.add_edge(f'{input_}', f'{result}')
				self.log.debug("Added variable node {0} and edge {0} -> {1}".format(input_, result))
			for cst_id_, input_ in enumerate(constants): # add a node for each input constant and the edge connecting it to result, each constant should have an unique identifier to distinguish
				cdfg.add_node(f'cst_{result}_{cst_id_}', id = self.dic_bbID[bbID], bbID = bbID,  type='constant', label=f'{input_}', value=f'{cst_id_}') # TODO: maybe we don't need the bitwidth for constant nodes, even for functional correctness reasons
				cdfg.add_edge(f'cst_{result}_{cst_id_}', f'{result}')
				self.log.debug("Added constant node {0} and edge {0} -> {1}".format(input_, result))

	# function to connect branch(es) with phi(s)
	def create_bb_control_signals(self):
		assert(self.dic_nodes != None) # check that the nodes dictionary has been already created
		if not("br" in self.dic_nodes) or not("phi" in self.dic_nodes): # check that phi(s) and branch(es) have been already included
			assert len(list(get_cdfg_nodes(self.cfg))) == 1, "Branch(es) and Phi(s) should be present if there are multiple BBs"
			return

		# branch_nodes_list = self.dic_nodes["br"]
		# phi_nodes_list = self.dic_nodes["phi"]
		# for branch_name in branch_nodes_list:
		# 	for phi_name in phi_nodes_list:
		# 		branch_node = self.cdfg.get_node(branch_name)
		# 		phi_node = self.cdfg.get_node(phi_name)
		# 		if branch_node.attr['bbID'] == phi_node.attr['bbID']:
		# 			self.cdfg = create_control_edge(self.cdfg, branch_node, phi_node)
		for e in get_cdfg_edges(self.cdfg):
			if self.is_backedge(e[0], e[1]):
				e.attr['style'] = 'dashed'

	#function to draw cdfg function representation of the ssa input file
	def draw_cdfg(self, output_file = 'test.pdf', layout = 'dot'):
		assert(not(self.cdfg is None))
		self.cdfg.draw(output_file, prog=layout) # drawing cdfg in the .pdf file
		self.cdfg.write(output_file.replace('.pdf', '.dot')) # describing cdfg in dot file
		self.log.info("Printed cdfg in file {0} with layout {1}. Its dot representation is in file {2}".format(output_file, layout, output_file.replace('.pdf','.dot')))
		cfg_filename = output_file.replace('.pdf', '.cfg.pdf')
		self.cfg.draw(cfg_filename, prog=layout) # drawing cfg in the .pdf file
		self.cfg.write(cfg_filename.replace('.pdf', '.dot')) # describing cfg in dot file
		self.log.info("Printed cfg in file {0} with layout {1}. Its dot representation is in file {2}".format(cfg_filename, layout, cfg_filename.replace('.pdf','.dot')))

	#function to get cdfg
	def get_cdfg(self):
		return self.cdfg

	#function to get cfg
	def get_cfg(self):
		return self.cfg
