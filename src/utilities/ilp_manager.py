import pulp as ilp
import logging
# function to check if `n` is a number or not
def is_number(n):
	if n == None:
		return False
	try:
		c = float(n)
		return True
	except ValueError:
		return False

############################################################################################################################################
############################################################################################################################################
#
#	`OPT_FUNCTION` CLASS
#
############################################################################################################################################
#	DESCRIPTION:
#				 The following class is used to describe the objective function of the ILP formulation
############################################################################################################################################
#	ATTRIBUTES:
#				- valid : validity of the objimizaiton function
#				- function_coeff : output objective function with coefficients
#				- ilp_obj : ILP object linked to objective function
#				- log: logger object used to output logs
############################################################################################################################################
#	FUNCTIONS:
#				- is_valid : returns the validity of the objective function
#				- add_variable : add variable and corresponding coefficient in the objective function
#				- remove_variable : remove variable in the objective function
#				- get_obj_function : get objective function
############################################################################################################################################
############################################################################################################################################

class Obj_Function:

	def __init__(self, ilp_obj, coeff_dict = None, log=None):
		if log != None:
			self.log = log
		else:
			self.log = logging.getLogger('obj_function') # if the logger is not given at object generation, create a new one
		assert(ilp_obj != None) # ilp_obj represents the ILP object to which the objective function belongs to
		self.valid = True
		self.function_coeff = {}
		self.ilp_obj = ilp_obj
		ilp_obj.set_objective_function(self)
		if coeff_dict == None: # the coefficients can be added later on
			return
		var_list = ilp_obj.get_variables_list() # if the coefficient dictionary is different from None, it is used to generate the first 
		for var in coeff_dict:
			if not(var in var_list):
				self.log.error("{0} is not a variable in the ILP object".format(var))
				self.valid = False
				return
		self.function_coeff = coeff_dict	

	# function to return validity of the objective function
	def is_valid(self):
		return self.valid

	# function to add a new variable and its corresponding coefficient in the objective function
	def add_variable(self, var_name, coeff=1):
		if not(self.valid):
			self.log.error("Obj_Function object is not valid!")
			return
		if not(var_name in self.ilp_obj.get_variables_list()):
			self.log.error("Variable not present in the ILP object")
			return
		if not(is_number(coeff)):
			self.log.error("Coefficient {0} is not numeric!".format(coeff))
			return
		if var_name in self.function_coeff:
			warning_string = "The variable {0} is already present in the objective function.".format(var_name)
			warning_string += "\nOld coefficient : {1}\nNew Coefficient : {2}".format(self.function_coeff[var_name], coeff)
			self.log.warning(warning_string)
		self.function_coeff[self.ilp_obj.get_variable(var_name)] = coeff
	
	# function to remove a variable from the objective function
	def remove_variable(self, var_name):
		assert(var_name in self.function_coeff)
		del self.function_coeff[var_name]

	# function to get the objective function
	def get_obj_function(self):
		return ilp.LpAffineExpression(e=self.function_coeff)


############################################################################################################################################
############################################################################################################################################
#
#	`CONSTRAINT_SET` CLASS
#
############################################################################################################################################
#	DESCRIPTION:
#				 The following class is used to describe the constraints of the ILP formulation
############################################################################################################################################
#	INFO:
#				'disequality_signs' is a dictionary that contains allowed signs for constraints
############################################################################################################################################
#	ATTRIBUTES:
#				- ilp_obj : ILP object linked to objective function
#				- constraints : set of constraints
#				- log: logger object used to output logs
############################################################################################################################################
#	FUNCTIONS:
#				- add_constraint : add contraint to constraints' set
#				- remove_constraint : remove constraint from constraints
#				- get_constraints : retrieve constraints' set
############################################################################################################################################
############################################################################################################################################

disequality_signs = {"eq":0, "geq":1, "leq":-1}

class Constraint_Set:

	def __init__(self, ilp_obj, log=None):
		if log != None:
			self.log = log
		else:
			self.log = logging.getLogger('constraint') # if the logger is not given at object generation, create a new one
		assert(ilp_obj != None) # ilp_obj represents the ILP object to which the objective function belongs to
		self.constraints = {}
		self.ilp_obj = ilp_obj
		ilp_obj.set_constraints(self)

	# function to add a new constraint
	def add_constraint(self, coeff_list, dis_sign, right_constant=0):
		constraint_id = "c{0}".format(len(self.constraints) + 1)
		constraint = {}
		for var_name in coeff_list:
			if not(type(var_name) is str):
				self.log.error("Variable {0} should be a string (the name of the variable)".format(var_name))
				return None
			if not(var_name in self.ilp_obj.get_variables_list()):
				self.log.error("Variable {0} not present in the ILP object".format(var_name))
				return None
			if not(dis_sign in disequality_signs):
				self.log.error("Disequality sign {0} is not allowerd. Allowed signs = {1}".format(dis_sign, disequality_signs.keys()))
				return None
			coefficient = coeff_list[var_name]
			if not(is_number(coefficient)):
				self.log.error("Coefficient {0} of variable {1} is not numeric".format(coeff_list[var_name], var_name))
				return None
			if not(is_number(right_constant)):
				self.log.error("Right Coefficient of the constraint {0} is not numeric".format(right_constant))
				return None
			# the constraint is a dictionary with variables as keys and coefficients as values
			constraint[self.ilp_obj.get_variable(var_name)] = coefficient
		# generation of constraint using the LpConstraint object
		constraint = ilp.LpConstraint(e=ilp.LpAffineExpression(e=constraint), sense=disequality_signs[dis_sign], name=constraint_id ,rhs=right_constant)
		self.constraints[constraint_id] = constraint
		return constraint_id
	
	# function to remove a constraint
	def remove_constraint(self, constraint_id):
		assert(constraint_id in self.constraints)
		del self.constraints[constraint_id]

	# function to retrieve constraints
	def get_constraints(self):
		return self.constraints

############################################################################################################################################
############################################################################################################################################
#
#	`ILP` CLASS
#
############################################################################################################################################
#	DESCRIPTION:
#				 The following class is used to interact with the ILP formulation
############################################################################################################################################
#	ATTRIBUTES:
#				- solver : ILP solver
#				- model_name : name of the ILP model
#				- model_minimize : model objective function should be minimized or maximized
#				- model : ILP model
#				- variables : ILP variables
#				- obj_function : objective function
#				- constraints : constraints set
#				- status : status of the ILP solution
#				- log: logger object used to output logs
############################################################################################################################################
#	FUNCTIONS:
#				- set_solver : set the ILP solver
#				- get_solver : get the ILP solver
#				- add_variable : add an ILP variable
#				- remove_variable : remove an ILP variable
#				- get_variable : get a variable
#				- get_variables_list : get the list of variables
#				- set_objective_function : set the objective function
#				- update_model : update the model with a constraint set and an objective function
#				- solve_ilp	: solve the ILP formulation
#				- reset_model : reset the ILP model
#				- print_ilp : print the ILP formulation
#				- get_ilp_solution : get ILP solution
#				- get_II_solution : get the II of the solution
#				- get_max_latency_solution : get the maximum latency of the solution
#				- get_variables_solution : get the list of variables happening in a specific clock
#				- get_operation_timing_solution : get the timing chosen from operation
############################################################################################################################################
############################################################################################################################################


class ILP:

	def __init__(self, solver="PULP_CBC_CMD", minimize=True, log=None):
		if log != None:
			self.log = log
		else:
			self.log = logging.getLogger('parser') # if the logger is not given at object generation, create a new one
		self.set_solver(solver)
		self.model_name = "ILP_model"
		self.model_minimize = minimize
		if minimize:
			self.model = ilp.LpProblem(self.model_name, ilp.LpMinimize)
		else:
			self.model = ilp.LpProblem(self.model_name, ilp.LpMaximize)
		self.variables = {}
		self.constraints = None
		self.obj_function = None
		self.status = None

	# function to set the solver
	def set_solver(self, solver="PULP_CBC_CMD"):
		list_solvers = ilp.listSolvers()
		assert(solver in list_solvers) #check that the solver is in the solver list
		self.solver = solver

	# function to get the solver
	def get_solver(self):
		return self.solver
	
	# function to add an ILP variable
	def add_variable(self, var_name, lower_bound = None, upper_bound = None, var_type = 'c'):
		assert(not(var_name in self.variables)) # check that var_name is not in the list of variables
		assert(is_number(upper_bound) or upper_bound == None) # assert that upper bound is numeric or None
		assert(is_number(lower_bound) or lower_bound == None) # assert that lower bound is numeric or None
		var_type_dic = {'i':"Integer", 'b': "Binary", 'c':"Continuous"} # dictionary to associate char to var_type
		if not(var_type in var_type_dic):
			self.log.error("ILP variable has only 3 var_type: i(nteger), b(inary) and c(continuous)")
			return
		var = ilp.LpVariable(var_name, lower_bound, upper_bound, var_type_dic[var_type])
		self.variables[var_name] = var
	
	# function to remove an ILP variable
	def remove_variable(self, var_name):
		assert(var_name in self.variables) # check that the variable is in the list of variables
		del self.variables[var_name]

	# function to get a variable
	def get_variable(self, var_name):
		assert(var_name in self.variables) # the var_name should be in the dictionary of variables
		return self.variables[var_name]

	# function to retrieve variables
	def get_variables_list(self):
		return self.variables

	# function to set objective function
	def set_objective_function(self, obj_function):
		if not(type(obj_function) is Obj_Function): # check that the objective function is an object of the class Obj_Function
			self.log.error("Objimization Function needs to be object of the class Obj_Function")
			return 
		self.obj_function = obj_function

	# function to set constraints' set
	def set_constraints(self, constraints):
		if not(type(constraints) is Constraint_Set): # check that the constraints is an object of the class Constraint_Set
			self.log.error("Constraints need to be object of the class Constraint_Set")
			return 
		self.constraints = constraints

	# function to update the model with a constraint set and an objective function
	def update_model(self, model, constraints_set, obj_function):
		assert(not(model is None)) # check that model is not None
		assert(not(constraints_set is None)) # check that constraints' set is not None
		assert(not(obj_function is None) and obj_function.is_valid()) # check the objective function is not None and the objective function is valid
		constraints = constraints_set.get_constraints()
		for constraint_id in constraints:
			model += constraints[constraint_id] , constraint_id # adding contraint in the model
		model += obj_function.get_obj_function(), "Objective_Function" # adding objective function in the model
		return model

	# function to solve the ILP formulation
	def solve_ilp(self):
		self.reset_model()
		self.model = self.update_model(self.model, self.constraints, self.obj_function)
		solver = ilp.getSolver(self.get_solver(), msg=0) # msg=0 enforces no output of the ILP solver
		self.status = self.model.solve(solver)
		if(self.status != 1):
			self.log.warning("ILP problem cannot be solved (Status {0})\t['-1': infeasible, '-2': unbounded, '-3': undefined]".format(self.status))
		return self.status

	# function to reset the ILP model
	def reset_model(self):
		if self.model_minimize:
			self.model = ilp.LpProblem(self.model_name, ilp.LpMinimize)
		else:
			self.model = ilp.LpProblem(self.model_name, ilp.LpMaximize)

	# function to print the ILP formulation
	def print_ilp(self, output_file="output.lp"):
		if self.model_minimize:
			model = ilp.LpProblem(self.model_name, ilp.LpMinimize)
		else:
			model = ilp.LpProblem(self.model_name, ilp.LpMaximize)
		model = self.update_model(model, self.constraints, self.obj_function)
		model.writeLP(output_file)
		self.log.info("The ILP formulation is written in "+output_file)

	# function to get ILP solution
	def get_ilp_solution(self):
		assert self.status != None and self.status == 1, "The function `solve_ilp` has to be called before using `get_ilp_solution` and its result has to be valid" # check that the ILP solution is valid
		result = {}
		for var_name in self.variables:
			result[var_name] = self.variables[var_name].varValue
		return result

	# function to get ILP solution II
	def get_II_solution(self):
		assert self.status != None and self.status == 1, "The function `solve_ilp` has to be called before using `get_ilp_solution` and its result has to be valid" # check that the ILP solution is valid
		assert "II" in self.variables, "II should be initiated as a variable in the ILP"
		return self.variables["II"].varValue

	# function to get ILP solution max_latency
	def get_max_latency_solution(self):
		assert self.status != None and self.status == 1, "The function `solve_ilp` has to be called before using `get_ilp_solution` and its result has to be valid" # check that the ILP solution is valid
		max_latency = -1
		for var_name in self.variables:
			if var_name != "II" and self.variables[var_name].varValue > max_latency:
				max_latency = self.variables[var_name].varValue
		assert max_latency != -1 , "Max latency should not be null"
		return max_latency

	# function to get ILP solution variables whose value is equal to a certain value 
	def get_variables_solution(self, clock):
		assert self.status != None and self.status == 1, "The function `solve_ilp` has to be called before using `get_ilp_solution` and its result has to be valid" # check that the ILP solution is valid
		result = []
		for var_name in self.variables:
			if var_name != "II" and self.variables[var_name].varValue == clock:
				result.append(var_name.replace("sv",""))
		return result

	# function to get ILP solution of the timing of an operation
	def get_operation_timing_solution(self, operation):
		assert self.status != None and self.status == 1, "The function `solve_ilp` has to be called before using `get_ilp_solution` and its result has to be valid" # check that the ILP solution is valid
		var_name = f'sv{operation}'
		assert var_name in self.variables, "{var_name} should be initiated as a variable in the ILP"
		return self.variables[var_name].varValue