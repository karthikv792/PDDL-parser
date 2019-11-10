import sys
import tarski
import tarski.io
from tarski.io.fstrips import print_init, print_goal, print_formula, print_atom
from tarski.syntax import CompoundFormula, formulas, Tautology, Atom
from tarski.fstrips import AddEffect, DelEffect
from tarski.fstrips.fstrips import FunctionalEffect
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
    model_dict = {}
    model_dict[PREDICATES] = store_predicates(reader)
    model_dict[FUNCTIONS] = store_functions(reader)
    model_dict[INSTANCE] = {}
    model_dict[INSTANCE][INIT] = {}
    model_dict[INSTANCE][INIT][FUNCTIONS], model_dict[INSTANCE][INIT][PREDICATES] = store_init(reader)
    model_dict[INSTANCE][GOAL] = store_goal(reader)
    model_dict[DOMAIN] = store_actions(reader)
    print(reader.problem.metric())
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
        predicates_list.append([preds.symbol,[sorts.name for sorts in preds.sort]])
    return predicates_list
def store_functions(reader):
    functions = list(reader.problem.language.functions)
    functions_list = []
    for funcs in functions:
        if funcs.symbol in ['ite','@','+','-','*','/','**','%','sqrt']:
            continue
        functions_list.append([funcs.symbol,[sorts.name for sorts in funcs.sort]])
    return functions_list
def store_init(reader):
    # print(dir(reader.problem))
    inits = reader.problem.init.as_atoms()
    init_dict = {}
    init_dict[FUNCTIONS] = []
    init_dict[PREDICATES] = []
    # for i in inits:
    #     if isinstance(i, Atom):
    #         init_dict.append([i.symbol,i.symbol.sort])
    init_list = []
    for i in range(len(inits)):
        if not isinstance(inits[i],Atom):
            if 'subterms' not in dir(inits[i][0]):
                init_dict[FUNCTIONS].append([inits[i][0].symbol,inits[i][1].symbol])
        else:
            if len(inits[i].subterms) == 0:
                init_dict[PREDICATES].append([inits[i].symbol,[subt.symbol for subt in inits[i].subterms]])
            else:
                init_dict[PREDICATES].append([inits[i].symbol,[]])
    return init_dict[FUNCTIONS], init_dict[PREDICATES]

def store_goal(reader):
    # print(reader.problem.goal.subformulas[0].subterms[0].symbol)
    # print(dir(reader.problem.goal.subformulas[0].subterms[0].symbol))
    goal = reader.problem.goal
    goals = []
    for subformula in goal.subformulas:
        goals.append([subformula.symbol, [i.symbol for i in subformula.subterms]])
    return goals
def store_actions(reader):
    action_model = {}
    for act in reader.problem.actions.values():
        action_model[act.name] = {}
        # Add parameter list
        action_model[act.name][PARARMETERS] = [(p.symbol.replace('?',''), p.sort.name) for p in act.parameters]
        if isinstance(act.precondition, CompoundFormula):
            action_model[act.name][POS_PREC] = [[subformula.symbol,[i.symbol for i in subformula.subterms]] for subformula in act.precondition.subformulas]
            # action_model[act.name][POS_PREC] = set([remove_parenthesis_from_name(print_formula(f))
            #                                         for f in act.precondition.subformulas])
        elif isinstance(act.precondition, formulas.Atom):
            # print(act.precondition)
            action_model[act.name][POS_PREC] = [[act.precondition.symbol, [i.symbol for i in act.precondition.subterms]]]
        else:
            action_model[act.name][POS_PREC] = []
        action_model[act.name][ADDS] = []
        action_model[act.name][DELS] = []
        action_model[act.name][FUNCTIONAL] = []
        action_model[act.name][COND_ADDS] = []
        action_model[act.name][COND_DELS] = []
        # print(act.effects)
        for curr_effs in act.effects:
            if type(curr_effs) != list:
                curr_effs = [curr_effs]
            for eff in curr_effs:
                # print(eff.condition)
                #Check if not tautology
                if not isinstance(eff.condition, Tautology):
                    # Conditional effects should be of the form [[condition,eff]]
                    curr_condition = []
                    if isinstance(eff.condition, CompoundFormula):
                        curr_condition.append([[subformula.symbol, [i.symbol for i in subformula.subterms]] for subformula in eff.condition.subformulas])
                    elif isinstance(eff.condition, Atom):
                        curr_condition.append([[eff.condition.symbol, [i.symbol for i in eff.condition.subterms]]])
                    if isinstance(eff, AddEffect):
                        if len(eff.atom.subterms) == 0:
                            action_model[act.name][COND_ADDS].append([curr_condition,[eff.atom.symbol, [subt.symbol for subt in eff.atom.subterms]]])
                        else:
                            action_model[act.name][COND_ADDS].append([curr_condition,[eff.atom.symbol, []]])
                    elif isinstance(eff, DelEffect):
                        if len(eff.atom.subterms) == 0:
                            action_model[act.name][COND_DELS].append([curr_condition,[eff.atom.symbol, [subt.symbol for subt in eff.atom.subterms]]])
                        else:
                            action_model[act.name][COND_DELS].append([curr_condition,[eff.atom.symbol, []]])
                    elif isinstance(eff, FunctionalEffect):
                        if "+" in str(eff.condition.symbol):
                            action_model[act.name][FUNCTIONAL].append([[eff.lhs.symbol,eff.lhs.sort.name],[eff.rhs.symbol,eff.rhs.sort.name]])
                else:
                    if isinstance(eff, AddEffect):
                        if len(eff.atom.subterms) == 0:
                            action_model[act.name][ADDS].append([eff.atom.symbol, [subt.symbol for subt in eff.atom.subterms]])
                        else:
                            action_model[act.name][ADDS].append([eff.atom.symbol, []])
                    if isinstance(eff, DelEffect):
                        if len(eff.atom.subterms) == 0:
                            action_model[act.name][DELS].append([eff.atom.symbol, [subt.symbol for subt in eff.atom.subterms]])
                        else:
                            action_model[act.name][DELS].append([eff.atom.symbol, []])

    return action_model







if __name__ == '__main__':
    parse_model('domain.pddl','problem.pddl')
