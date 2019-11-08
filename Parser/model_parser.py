import sys
import tarski
import tarski.io
from tarski.io.fstrips import print_init, print_goal, print_formula, print_atom
from tarski.syntax import CompoundFormula, formulas, Tautology
from tarski.fstrips import AddEffect, DelEffect
from constants import *


def remove_parenthesis_from_name(full_name):
    '''
    For action and predicate names
    '''
    # TODO: Figure out why tarski is producing double ??
    return full_name.strip().replace('(', '').replace(')', '').replace('??', '?').strip()


def parse_model(domain_file, problem_file):
    # Assume the problem and domain is fully grounded
    # Read the pddl files
    curr_reader = tarski.io.FstripsReader()
    curr_reader.read_problem(domain_file, problem_file)
    pred1 = {}
    preds = curr_reader.problem.language._predicates
    # print(preds['alerted'].sort[0].name,preds['alerted'].symbol)
    for key, value in preds.items():
        v = (value.symbol,value.sort)
        pred1[key]=v
    # print(pred1)
    func = {}
    funcs = curr_reader.problem.language.functions
    for i in funcs:
        # print(i.sort)
        func[i] = [i.symbol,[j.name for j in i.sort]]


    # Make the sets for init and goal
    init_set = set([remove_parenthesis_from_name(fact) for fact in print_init(curr_reader.problem).split("\n")])
    assert isinstance(curr_reader.problem.goal, CompoundFormula) or isinstance(curr_reader.problem.goal, formulas.Atom)
    if isinstance(curr_reader.problem.goal, CompoundFormula):
        goal_set = set([remove_parenthesis_from_name(print_formula(fact))
                        for fact in curr_reader.problem.goal.subformulas])
    else:
        goal_set = set([remove_parenthesis_from_name(print_formula(curr_reader.problem.goal))])
    # Make the dictionary for actions
    # print(curr_reader)
    action_model = {}
    for act in curr_reader.problem.actions.values():
        action_model[act.name] = {}
        # Add parameter list
        action_model[act.name][PARARMETERS] = [(p.symbol.replace('?',''), p.sort.name) for p in act.parameters]
        #print(list(action_model[act.name][PARARMETERS]))
        #print(act.parameters)

        # Make sure the precondition is just a simple conjunction of positive literals
        #assert isinstance(act.precondition, CompoundFormula) or isinstance(act.precondition,formulas.Atom) or isinstance(act.precondition, formulas.Tautology)
        if isinstance(act.precondition, CompoundFormula):
            action_model[act.name][POS_PREC] = set([remove_parenthesis_from_name(print_formula(f))
                                                    for f in act.precondition.subformulas])
        elif isinstance(act.precondition, formulas.Atom):
            action_model[act.name][POS_PREC] = set([remove_parenthesis_from_name(print_atom(act.precondition))])
        else:
            action_model[act.name][POS_PREC] = set()
        # Parse effects
        action_model[act.name][ADDS] = set()
        action_model[act.name][DELS] = set()
        action_model[act.name][INCREMENT] = []
        action_model[act.name][COND_ADDS] = []
        action_model[act.name][COND_DELS] = []
        for curr_effs in act.effects:
            if type(curr_effs) != list:
                curr_effs = [curr_effs]
            for eff in curr_effs:
                # Todo: For some reason tarski is generating None effects
                if eff:
                    conditional = not isinstance(eff.condition, Tautology)
                    if conditional:
                        # Conditional effects should be of the form [[condition,eff]]
                        curr_condition = []
                        print(dir(eff))
                        print(eff.condition.symbol)
                        #assert isinstance(eff.condition, CompoundFormula) or isinstance(eff.condition,formulas.Atom)
                        if isinstance(eff.condition, CompoundFormula):
                            for f in eff.condition.subformulas:
                                curr_condition.append(remove_parenthesis_from_name(print_formula(f)))
                        elif isinstance(eff.condition, formulas.Atom):
                            curr_condition.append(remove_parenthesis_from_name(print_atom(eff.condition)))

                        if isinstance(eff, AddEffect):
                            action_model[act.name][COND_ADDS].append(
                                [curr_condition, remove_parenthesis_from_name(print_atom(eff.atom))])
                        elif isinstance(eff, DelEffect):
                            action_model[act.name][COND_DELS].append(
                                [curr_condition, remove_parenthesis_from_name(print_atom(eff.atom))])
                        elif isinstance(eff, tarski.fstrips.fstrips.FunctionalEffect):
                            if "+" in str(eff.condition.symbol):
                                action_model[act.name][INCREMENT].append((str(eff.lhs), str(eff.rhs)))

                    else:
                        if isinstance(eff, AddEffect):
                            action_model[act.name][ADDS].add(remove_parenthesis_from_name(print_atom(eff.atom)))
                        elif isinstance(eff, DelEffect):
                            action_model[act.name][DELS].add(remove_parenthesis_from_name(print_atom(eff.atom)))
    model_dict = {}
    model_dict[DOMAIN] = action_model
    model_dict[PREDICATES] = []
    model_dict[FUNCTIONS] = []
    model_dict[INSTANCE] = {}
    model_dict[INSTANCE][INIT] = init_set
    model_dict[INSTANCE][GOAL] = goal_set
    return model_dict


if __name__ == '__main__':
    domain_file = sys.argv[1]
    problem_file = sys.argv[2]
