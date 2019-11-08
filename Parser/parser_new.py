import sys
import tarski
import tarski.io
from tarski.io.fstrips import print_init, print_goal, print_formula, print_atom
from tarski.syntax import CompoundFormula, formulas, Tautology, Atom
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

    store_goal(reader)
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
    predicates = list(reader.problem.language.predicates)
    functions = list(reader.problem.language.functions)
    inits = reader.problem.init.as_atoms()
    init_dict = {}
    init_dict[FUNCTIONS] = []
    init_dict[PREDICATES] = []
    # for i in inits:
    #     if isinstance(i, Atom):
    #         init_dict.append([i.symbol,i.symbol.sort])
    print(dir(inits[62][1]))
    init_list = []
    for i in range(len(inits)):
        if inits[i].symbol in functions:
            if subterms not in dir(inits[i][0]):
                init_dict[FUNCTIONS].append([inits[i][0].symbol,inits[i][1].symbol])
        elif inits[i].symbol in predicates:
            if isinstance(inits[i],Atom):
                if len(inits[i].subterms) == 0:
                    init_dict[PREDICATES].append([inits[i].symbol,[subt for subt in inits[i].subterms]])
                else:
                    init_dict[PREDICATES].append([inits[i].symbol])
    return init_dict[FUNCTIONS], init_dict[PREDICATES]

def store_goal(reader):
    print(reader.problem.goal)
    print(dir(reader.problem.goal))






if __name__ == '__main__':
    parse_model('domain.pddl','problem.pddl')
