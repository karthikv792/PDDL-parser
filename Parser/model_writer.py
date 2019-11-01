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
        self.fstrips_problem = create_fstrips_problem(language(),"test_domain", "instance1")
        self.fluent_set_map = {}
        self.count = 1
        self.populate_fstrips_object()

    def add_predicates_to_the_prob(self, fluent):
        # TODO: Assuming only propositional models

        if fluent not in self.fluent_set_map:
            print("%d COunter",self.count)
            print(fluent)
            predicate = self.model_dict[PREDICATES][fluent]

            # Add to tarski list

            pred_obj = self.fstrips_problem.language.predicate(predicate[0])
            print("PRED OBJECT", pred_obj)
            self.fluent_set_map[fluent] = pred_obj
            self.count+=1
        return self.fluent_set_map[fluent]

    def add_types_to_the_prob(self, var, type):
        pass

    def get_conjunctions(self, fluent_list):
        if len(fluent_list) == 0:
            return top
        if len(fluent_list) <= 1:
            return self.add_predicates_to_the_prob(list(fluent_list)[0])()
        else:
            try:
                return land(*[self.add_predicates_to_the_prob(fl)() for fl in fluent_list])
            except AssertionError as exc:
                raise Exception("Message:",exc," Original fluent set", fluent_list)

    def populate_fstrips_object(self):
        # Populate initial state
        for init_val in self.model_dict[INSTANCE][INIT]:
            self.add_predicates_to_the_prob(init_val)
            self.fstrips_problem.init.add(self.add_predicates_to_the_prob(init_val))
        # populate goal state
        self.fstrips_problem.goal = self.get_conjunctions(self.model_dict[INSTANCE][GOAL])
        # populate action models
        for act in self.model_dict[DOMAIN]:
            act_name = act
            # Only pos
            precond = self.get_conjunctions(self.model_dict[DOMAIN][act][POS_PREC])
            add_effects = [fs.AddEffect(self.add_predicates_to_the_prob(fl)()) for fl in self.model_dict[DOMAIN][act].get(ADDS,set())]
            delete_effects = [fs.DelEffect(self.add_predicates_to_the_prob(fl)())
                              for fl in self.model_dict[DOMAIN][act].get(DELS,set())]
            if PARARMETERS in self.model_dict[DOMAIN][act]:
                pars = []
                for p,s in self.model_dict[DOMAIN][act][PARARMETERS]:
                    try:
                        sort = self.fstrips_problem.language.get_sort(s)
                    except UndefinedSort:
                        sort = self.fstrips_problem.language.sort(s)
                    pars.append(self.fstrips_problem.language.variable(p,sort))

                #pars = [self.fstrips_problem.language.variable(p,self.fstrips_problem.language.sort(s)) for p,s in self.model_dict[DOMAIN][act][PARARMETERS]]
                #print(pars)
            else:
                pars = []
            self.fstrips_problem.action(act_name, pars, precond, add_effects + delete_effects)

    def write_files(self, domain_file, problem_file):
        curr_writer = FstripsWriter(self.fstrips_problem)
        curr_writer.write(domain_file, problem_file)
