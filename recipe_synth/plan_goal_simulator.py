from unified_planning.shortcuts import (
    SequentialSimulator,
    FluentExp,
    Problem
)
from unified_planning.plans import SequentialPlan

import pandas as pd

def simulate(
        plan:SequentialPlan,
        sim: SequentialSimulator,
        problem: Problem
    ):
    # Assumption: Users want to monitor progress towards goals
    headers = ["action"]
    goal_expression = []
    # Create a fluent expressions from the entities found in the goals
    for goal in problem.goals:
        for domn_obj in problem.all_objects:
            for goal_arg in goal.args:
                if domn_obj.name in str(goal_arg) and not domn_obj.name in headers:
                    headers.append(domn_obj.name)
                    #TODO: This seems quite fragile. It makes assumptions about the arity and the argument type
                    for flt in problem.fluents:
                        if domn_obj.type.name == flt.signature[0].type.name:
                            goal_expression.append(FluentExp(flt, domn_obj)) # How to get the matching fluent?

    initial_state = sim.get_initial_state()
    current_state = initial_state
    # We also store the states to plot the metrics later
    states = [current_state]
    rows = []
    for action_instance in plan.actions:
        current_state = sim.apply(current_state, action_instance)
        if current_state is None:
            print(f'Error in applying: {action_instance}')
            break
        states.append(current_state)
        row = [action_instance]
        for expr in goal_expression:
            row.append(current_state.get_value(expr).constant_value())
        rows.append(row)
    
    df = pd.DataFrame(rows, columns=headers)
    print("\n")
    print(df)