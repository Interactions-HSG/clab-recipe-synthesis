from unified_planning.shortcuts import (
    SequentialSimulator,
    Fluent,
    Object,
    FluentExp,
    Problem
)
from unified_planning.plans import SequentialPlan

import pandas as pd


def simulate_b2p(
        plan:SequentialPlan,
        sim: SequentialSimulator,
        problem: Problem,
    ):
    por = (0, 16,) # pixel object range
    pixel_occupied = list(FluentExp(problem.fluent("occupied"), obj) for obj in problem.all_objects[por[0]:por[1]])
    pixel_occupied_by = list(FluentExp(problem.fluent("occupied_by"), obj) for obj in problem.all_objects[por[0]:por[1]])
    

    headers = [
        "action",
        # f"{problem.fluents[2].name}({problem.all_objects[4]})",
        # # f"{problem.fluents[1].name}({problem.all_objects[4]})",
        "--",
        "--",
        "--",
        "--",
        "#b1",
        "#b2"
    ]
    initial_state = sim.get_initial_state()
    current_state = initial_state
    # We also store the states to plot the metrics later
    states = [current_state]
    rows = []
    # Looking for BlockVar1 and BlockVar2. Found no way to parameterize
    inv = list(FluentExp(problem.fluent("block_inv"), obj) for obj in problem.all_objects[16:18])
    b1 = current_state.get_value(inv[0]).constant_value()
    b2 = current_state.get_value(inv[1]).constant_value()

    for i in range(4):
        if 0 == i:
            rows.append(["initial state", "x0", "x1", "x2", "x3", b1, b2])
        rows.append([f"y{i}", "" , "", "", "", "", "" ])
    rows.append([""] * 7)

    for action_instance in plan.actions:
        sec_rows = []
        current_state = sim.apply(current_state, action_instance)
        if current_state is None:
            print(f'Error in applying: {action_instance}')
            break
        states.append(current_state)
        b1 = current_state.get_value(inv[0]).constant_value()
        b2 = current_state.get_value(inv[1]).constant_value()
        for i in range(4):
            if 0 == i:
                sec_rows.append([action_instance, "x0", "x1", "x2", "x3", b1, b2])
            sec_rows.append([f"y{i}", "" , "", "", "", "", "" ])
        rows.append([""] * 7)

        for occupied in pixel_occupied:
            name = next(iter(occupied.args[0].get_contained_names()))
            blk_id = 0
            for occupied_by in pixel_occupied_by:
                if occupied_by.args[0] == occupied.args[0]:
                    blk_id = current_state.get_value(occupied_by).constant_value()
                    break
            _, x, y = name.split("_")
            sec_rows[1+int(y)][1+int(x)] = f"b{blk_id}" if blk_id else ""

        for row in sec_rows:
            rows.append(row)
    
    df = pd.DataFrame(rows, columns=headers)
    pd.set_option('display.max_rows', 999)
    pd.set_option('display.max_columns', 999)
    pd.set_option('display.width', 999)
    print("\n")
    print(df)


def simulate_fb(
        plan:SequentialPlan,
        sim: SequentialSimulator,
        problem: Problem,
    ):
    goal_expression = [
        FluentExp(problem.fluents[0], problem.all_objects[4]),
        FluentExp(problem.fluents[1], problem.all_objects[4])
    ]
    headers = [
        "action",
        "",
        "0",
        "1",
        "2",
        "3",
    ]
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



def simulate(
        plan:SequentialPlan,
        sim: SequentialSimulator,
        problem: Problem,
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
        # for flt in problem.fluents:
        #     for goal_arg in goal.args:
        #         if flt.name in str(goal_arg) and not flt.name in headers:
        #             headers.append(flt.name)
        #             #TODO: This seems quite fragile. It makes assumptions about the arity and the argument type
        #             for domn_obj in problem.all_objects:
        #                 if domn_obj.type.name == flt.signature[0].type.name:
        #                     goal_expression.append(FluentExp(flt, domn_obj)) # How to get the matching fluent?

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