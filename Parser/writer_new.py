from constants import *
from tarski import fstrips as fs
from tarski.fstrips.problem import create_fstrips_problem
from tarski.fstrips import language
from tarski.syntax import land, top,VariableBinding
from tarski.io.fstrips import FstripsWriter
from tarski.errors import UndefinedSort

class ModelWriter(object):
    def __init__(self, model):
        self.model_dict = model
        self.predicate_map = {}
        self.functions = {}
        self.fstrips_problem = create_fstrips_problem(language(), "instance1","test_domain")
        self.create_hierarchy()
        self.create_predicates()
        self.create_functions()
        self.write_init()
        self.write_goal()

    def create_hierarchy(self):
        ancestors = self.model_dict[HIERARCHY][ANCESTORS]
        imm_parents = self.model_dict[HIERARCHY][IMM_PARENT]
        # # print(ancestors)
        # # print(imm_parents)
        # for parent in imm_parents:
        #
        # for ancestor in ancestors:
        #
        #     try:
        #         sort = self.fstrips_problem.language.get_sort(ancestor[0])
        #     except UndefinedSort:
        #         sort = self.fstrips_problem.language.sort(ancestor[0][0],)
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
            # print(self.functions[function[0]],function[1])
            self.fstrips_problem.init.set(function[0],*[function[1][0]])
        for predicate in predicates:
            self.fstrips_problem.init.add(predicate[0],*predicate[1])
    def write_goal(self):
        goal = self.model_dict[INSTANCE][GOAL]
        print(dir(self.fstrips_problem.goal))
        # if len(goal) == 0:
        #     return top
        # if len(goal) <= 1:
        #     return self.add_predicates_to_the_prob(list(fluent_list)[0])(*)
        # else:
        #     try:
        #         return land(*[self.add_predicates_to_the_prob(fl) for fl in fluent_list])
        #     except AssertionError as exc:
        #         raise Exception("Message:", exc, " Original fluent set", fluent_list)

    def write_files(self, domain_file, problem_file):
        curr_writer = FstripsWriter(self.fstrips_problem)
        curr_writer.write(domain_file, problem_file)
