from constants import *
from tarski import fstrips as fs
from tarski import model
from tarski.fstrips.problem import create_fstrips_problem
from tarski.io.fstrips import print_init, print_goal, print_formula, print_atom
from tarski.fstrips import language
from tarski.syntax import land, top,VariableBinding
from tarski.io.fstrips import FstripsWriter
from tarski.errors import UndefinedSort

class ModelWriter(object):
    def __init__(self, model):
        self.model_dict = model
        self.predicate_map = {}
        self.functions = {}
        self.variable_map={}
        self.fstrips_problem = create_fstrips_problem(language(), "instance1","test_domain")
        self.create_hierarchy()
        self.create_predicates()
        self.add_constants()
        self.create_functions()
        self.write_init()
        self.write_goal()
        self.write_actions()
        # print([act.precondition for act in self.fstrips_problem.actions.values()])

    def create_hierarchy(self):
        ancestors = self.model_dict[HIERARCHY][ANCESTORS]
        imm_parents = self.model_dict[HIERARCHY][IMM_PARENT]
        for obj in imm_parents:
            try:
                sort = self.fstrips_problem.language.get_sort(obj[0])
            except UndefinedSort:
                self.fstrips_problem.language.sort(obj[0],obj[1])
        # print(self.fstrips_problem.language.ancestor_sorts)

    def create_predicates(self):
        predicates = self.model_dict[PREDICATES]
        for predicate in predicates:
            sorts=[]
            for s in predicate[1]:
                try:
                    sort = self.fstrips_problem.language.get_sort(s)
                except UndefinedSort:
                    sort = self.fstrips_problem.language.sort(s)
                sorts.append(sort)
            pred_obj = self.fstrips_problem.language.predicate(predicate[0], *sorts)
            self.predicate_map[predicate[0]] = pred_obj
        # print(self.fstrips_problem.language.predicates)

    def add_constants(self):
        constants = self.model_dict[CONSTANTS]
        # print(constants)
        for constant in constants:
            try:
                sort = self.fstrips_problem.language.get_sort(constant[1])
            except UndefinedSort:
                sort = self.fstrips_problem.language.sort(constant[1])
            self.fstrips_problem.language.constant(constant[0],sort)


    def create_functions(self):
        # print(self.predicate_map)
        functions = self.model_dict[FUNCTIONS]
        # print(functions)
        for function in functions:
            sorts = []
            for s in function[1]:
                try:
                    sort = self.fstrips_problem.language.get_sort(s)
                except UndefinedSort:
                    sort = self.fstrips_problem.language.sort(s)
                sorts.append(sort)
            func_obj = self.fstrips_problem.language.function(function[0],*sorts)
            self.functions[function[0]] = func_obj

    def write_init(self):
        functions = self.model_dict[INSTANCE][INIT][FUNCTIONS]
        predicates = self.model_dict[INSTANCE][INIT][PREDICATES]
        for function in functions:
            # print(function[0],function[1])
            self.fstrips_problem.init.set(function[0],*[function[1][0]])
        for predicate in predicates:
            self.fstrips_problem.init.add(self.predicate_map[predicate[0].symbol],*predicate[1])

    def get_goals(self,fluent_list):
        temp_model = model.create(self.fstrips_problem.language)
        if len(fluent_list)==0:
            return top
        elif len(fluent_list)<=1:
            temp_model.add(self.predicate_map[fluent_list[0][0].symbol], *fluent_list[0][1])
            return temp_model.as_atoms()
        else:
            try:
                for subgoal in fluent_list:
                    temp_model.add(self.predicate_map[subgoal[0].symbol], *subgoal[1])
                return land(*temp_model.as_atoms())
            except AssertionError as exc:
                raise Exception("Message:", exc, " Original fluent set", fluent_list)



    def write_goal(self):
        goal = self.model_dict[INSTANCE][GOAL]
        self.fstrips_problem.goal = self.get_goals(goal)

# ACTIONS
    def get_conjunctions(self,fluent_list,flag):
        if len(fluent_list)==0:
            if flag==POS_PREC:
                return top
            else:
                return []
        elif len(fluent_list)<=1:
            fluent = fluent_list[0]
            variables = fluent[1]
            var = [self.variable_map[variable.replace('?','')] for variable in variables]
            if flag==POS_PREC:
                return self.predicate_map[fluent[0].symbol](*var)
            elif flag==ADDS:
                return [fs.AddEffect(self.predicate_map[fluent[0].symbol](*var))]
            elif flag==DELS:
                return [fs.DelEffect(self.predicate_map[fluent[0].symbol](*var))]
        else:
            and_fluent_list=[]
            if flag==POS_PREC:
                for fluent in fluent_list:
                    variables = fluent[1]
                    var = [self.variable_map[variable.replace('?','')] for variable in variables]
                    and_fluent_list.append(self.predicate_map[fluent[0].symbol](*var))
                return land(*and_fluent_list)
            elif flag==ADDS:
                for fluent in fluent_list:
                    variables = fluent[1]
                    var = [self.variable_map[variable.replace('?','')] for variable in variables]
                    and_fluent_list.append(fs.AddEffect(self.predicate_map[fluent[0].symbol](*var)))
                return and_fluent_list
            elif flag==DELS:
                for fluent in fluent_list:
                    variables = fluent[1]
                    var = [self.variable_map[variable.replace('?','')] for variable in variables]
                    and_fluent_list.append(fs.DelEffect(self.predicate_map[fluent[0].symbol](*var)))
                return and_fluent_list



    def write_actions(self):
        actions = self.model_dict[DOMAIN]
        for act in self.model_dict[DOMAIN]:

            if PARARMETERS in self.model_dict[DOMAIN][act]:
                pars = []
                for p, s in self.model_dict[DOMAIN][act][PARARMETERS]:
                    try:
                        sort = self.fstrips_problem.language.get_sort(s)
                    except UndefinedSort:
                        sort = self.fstrips_problem.language.sort(s)
                    new_var = self.fstrips_problem.language.variable(p, sort)
                    #ADDING VARIABLE TO VARIABLE MAP
                    if new_var.symbol in self.variable_map.keys():
                        pars.append(new_var)
                    else:
                        self.variable_map[new_var.symbol] = new_var
                        pars.append(new_var)
                precond = self.get_conjunctions(self.model_dict[DOMAIN][act][POS_PREC],POS_PREC)
                # print(self.model_dict[DOMAIN][act].get(ADDS,set()))
                # print(self.model_dict[DOMAIN][act].get(DELS, set()))
                add_effects = self.get_conjunctions(self.model_dict[DOMAIN][act].get(ADDS,set()),ADDS)
                delete_effects = self.get_conjunctions(self.model_dict[DOMAIN][act].get(DELS,set()),DELS)
            else:
                pars=[]
            self.fstrips_problem.action(act,pars,precond,add_effects+delete_effects)

    def write_files(self, domain_file, problem_file):
        curr_writer = FstripsWriter(self.fstrips_problem)
        curr_writer.write(domain_file, problem_file)
