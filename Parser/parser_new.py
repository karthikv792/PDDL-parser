import sys
import tarski
import tarski.io
from tarski.io.fstrips import print_init, print_goal, print_formula, print_atom
from tarski.syntax import CompoundFormula, formulas, Tautology
from tarski.fstrips import AddEffect, DelEffect
from constants import *

def parse_model(domain_file, problem_file):
    reader = tarski.io.FstripsReader()
    reader.read_problem(domain_file,problem_file)
    """Things to be read
        1. TYPES
        2. FUNCTIONS
        3. PREDICATES
        4. ACTIONS
    """

    store_init(reader)
    # print(reader.problem.language.predicates)
    # print(reader.problem.language.functions)
    # print(reader.problem.goal.subformulas)
    # print(list(reader.problem.actions.values())[0].name)
    # print(list(reader.problem.actions.values())[0].parameters)
    # print(print_atom(list(reader.problem.actions.values())[0].precondition))

def store_predicates(reader):
    predicates = list(reader.problem.language.predicates)
    predicates_list = []
    for preds in predicates:
        if preds.symbol in ['=','!=','<','<=','>','>=']:
            continue
        predicates_list.append([preds.name,[sorts.name for sorts in preds.sort]])
    return predicates_list
def store_functions(reader):
    functions = list(reader.problem.language.functions)
    functions_list = []
    for funcs in functions:
        if funcs.symbol in ['ite','@','+','-','*','/','**','%','sqrt']:
            continue
        functions_list.append([funcs.name,[sorts.name for sorts in funcs.sort]])
    return functions_list
def store_init(reader):
    # print(dir(reader.problem))
    inits = reader.problem.init.as_atoms()
    print((reader.problem.init.language.functions))
    init_list = []
    # for i in inits:
    #     init_list.append([i.symbol,])
    #     print(a,a.symbol.sort,(a.subterms[0].sort))



if __name__ == '__main__':
    parse_model('domain.pddl','problem.pddl')
