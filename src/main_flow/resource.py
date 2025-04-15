from src.utilities.ilp_manager import *
from src.utilities.cdfg_manager import *
import logging

############################################################################################################################################
############################################################################################################################################
#
#	`RESOURCE_MANAGER` CLASS
#
############################################################################################################################################
#	DESCRIPTION:
#					The following class is used for resource sharing in CDFG (Control DataFlow Graph) representing a function.
############################################################################################################################################
#	ATTRIBUTES:
#					- ilp : ILP problem of the class ILP
#					- constraint_set : set of constraints of the class CONSTRAINT_SET
#					- obj_function : optimization function of the class Obj_Function
#					- log: logger object used to output logs
############################################################################################################################################
#	FUNCTIONS:
# 					- add_resource_constraints : setting up the maximum resource usage per res type in the constraint set
#					- add_resource_constraints_pipelined : add resources constraints for pipelined scheduling
#					- check_resource_dict : validate values in resource dict
############################################################################################################################################
############################################################################################################################################

allowed_resources = ["load", "add", "mul", "div", "zext"]

class Resource_Manager:
	def __init__(self, parser, ilp_dependency_inj, log=None, ):
		assert(parser != None) # ensure Parser is different from None
		assert(ilp_dependency_inj != None) # ensure ilp source is different from None
		self.cdfg = parser.get_cdfg() # save the CDFG of the parser
		self.cfg = parser.get_cfg() # save the CFG of the parser
		if log != None:
			self.log = log
		else:
			self.log = logging.getLogger('resource') # if the logger is not given at object generation, create a new one
		
		ilp_dependency_inj(self)

	"""
	Adds scheduling ILP created by the Scheduler must be passed to the Resources
	"""
	def set_scheduling_ilp(self, ilp, constraints, obj_fun):
		self.ilp = ilp
		self.constraints = constraints
		self.obj_fun = obj_fun


	"""
	Adds constraints to the constraint set that enforce the resource constraints contained in the resource dictionary
	"""
	def add_resource_constraints(self, resource_dict):
		self.check_resource_dict(resource_dict)

		ordered_nodes = get_topological_order(self.cdfg)
		for bb in self.cdfg:
			for resource_type, max_units in resource_dict.items():
				resource_node = []
				for node in ordered_nodes:
					if node.attr.get("id") != bb.attr["id"]: # Not in current BB
						continue
					if node.attr.get("type") == resource_type: # Add all nodes of same resource
						resource_node.append(node)	
				
				for i in range(max_units, len(resource_node)):
					lhs_dictionary = {}
					lhs_dictionary[f"sv{resource_node[i]}"] = 1
					lhs_dictionary[f"sv{resource_node[i - max_units]}"] = -1

					self.constraints.add_constraint(lhs_dictionary, "geq", 1)	

	def add_resource_constraints1(self, resource_dict):

		self.check_resource_dict(resource_dict)
		
		# Obtain a topological ordering of nodes in the CDFG.
		sorted_nodes = get_topological_order(self.cdfg)
		
		# For each resource type defined in the dictionary, group nodes by basic block.
		for resource_type, max_units in resource_dict.items():
			# Dictionary to group nodes: key is basic block id; value is list of nodes.
			nodes_by_bb = {}
			for node in sorted_nodes:
				# Check if the node is of the given resource type.
				if node.attr.get("type") == resource_type:
					bb = node.attr.get("id")  # basic block id
					nodes_by_bb.setdefault(bb, []).append(node)
			
			# For each basic block, add ordering constraints among nodes of this resource type.
			for bb, nodes in nodes_by_bb.items():
				# We assume nodes are already in topological order.
				for i in range(max_units, len(nodes)):
					lhs_dictionary = {}
					# Use a consistent naming scheme (assumes that add_nodes_to_ilp uses node.attr['label'])
					later_var = f"sv{nodes[i].attr.get('label')}"
					earlier_var = f"sv{nodes[i - max_units].attr.get('label')}"
					lhs_dictionary[later_var] = 1
					lhs_dictionary[earlier_var] = -1
					
					# Add constraint: sv(later) - sv(earlier) >= 1
					self.constraints.add_constraint(lhs_dictionary, "geq", 1)



	# function to add resources constraints for pipelined scheduling
	def check_resource_constraints_pipelined(self, resource_dict, II):
		self.check_resource_dict(resource_dict)

		mrt = {}
		for i in range(II):
			mrt[i] = {}

		for node in self.cdfg:
			resource_node = node.attr.get("type")
			if resource_node not in resource_dict:
				continue

			col = self.ilp.get_operation_timing_solution(node) % II

			if resource_node in mrt[col]:
				mrt[col][resource_node] += 1
			else:
				mrt[col][resource_node] = 1

		for col in mrt:
			for res, count in mrt[col].items():
				if count > resource_dict[res]:
					return False
				
		return True

	"""
	Checks the types specified in the given resource dictionary(a dictionary containing something like "bogusoperationtype" wouldn't be valid) and sets the resource_dic member variable of the class to the specified resource dictionary
	@param resource_dic: the resource dictionary that the class should use
	"""
	def check_resource_dict(self, resource_dict):
		for resource in resource_dict:
			if not(resource in allowed_resources): # the resource type should be present in the list of allowed resource types
				self.log.error("Resource {0} is not allowed (allowed resources = {1})".format(resource, allowed_resources))
				continue