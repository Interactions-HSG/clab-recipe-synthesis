import os.path
from pathlib import Path as plibPath

# this is bad since it imports a Path object
from unified_planning.shortcuts import *
from unified_planning.model.metrics import MinimizeSequentialPlanLength

import to_pddl
import plan_goal_simulator


"""
This is a simple mock to show how a shape (piece) can be approximated using AI planning
"""
NPIXEL_X = 4
NPIXEL_Y = 4
problem = Problem('PieceToBlock')

Pixel = UserType("Pixel")
pos_x = Fluent("pos_x", IntType(), s=Pixel)
problem.add_fluent(pos_x, default_initial_value=0)
pos_y = Fluent("pos_y", IntType(), s=Pixel)
problem.add_fluent(pos_y, default_initial_value=0)
domain_obj_names = []
domain_objs = {}
pixel_objs = {}
for px_x in range(NPIXEL_X):
    for px_y in range(NPIXEL_Y):
        name = f"px_{px_x}_{px_y}"
        domain_obj_names.append(name)
        obj = problem.add_object(name, Pixel)
        domain_objs.update({name: obj})
        pixel_objs.update({name: obj})
        problem.set_initial_value(pos_x(obj), px_x)
        problem.set_initial_value(pos_y(obj), px_y)


function_count = Fluent("function_count", IntType())
occupied = Fluent("occupied", BoolType(), s=Pixel)
problem.add_fluent(occupied, default_initial_value=False)
# BlockVarType = UserType("BlockVarType")
# BlockInvType = UserType("BlockInvType")
# block_inv = Fluent("block_inv", IntType(), blk=BlockVarType)


# block_size_x = Fluent("block_size_x", IntType(), blk=BlockVarType)
# block_1_obj = Object("BlockVar_1", BlockVarType)
# problem.add_fluent(block_size_x, default_initial_value=1)
# problem.set_initial_value(block_size_x(block_1_obj), 1)

# occupies_x = Fluent("occupies_x", IntType(), blk=BlockVarType)
# occupies_y = Fluent("occupies_y", IntType(), blk=BlockVarType)


# pixel_1_Obj = Object("pixel_00", Pixel)
# pixel_2_Obj = Object("pixel_01", Pixel)
# problem.add_fluent(pos_x, default_initial_value=0)
# problem.add_fluent(pos_y, default_initial_value=0)
# problem.set_initial_value(pos_x(pixel_1_Obj), 0)
# problem.set_initial_value(pos_y(pixel_1_Obj), 0)

def make_goal_fn():
    goal_fn = InstantaneousAction(
        "goal_fn",
        # blk=BlockVarType,
        start_px=Pixel
    )
    # blk = goal_fn.parameter("blk")
    start_px = goal_fn.parameter("start_px")
    goal_fn.add_increase_effect(function_count, 1)
    # condition_forall(
    #     LE(
    #         pos_x(p),
    #         pos_x(start_pixel) + block_size_x(blk)
    #     ),
    #     (occupied(Variable("p", Pixel)) for _ in range(10))
    # )
    
    # forall_vars = {"p": Variable("p", Pixel)}
    # p = Variable("p", Pixel) 

    goal_fn.add_effect(
        # occupied(p),
        occupied(start_px),
        True,
        # forall=(p,),
        # condition=(Not(occupied(p)))
    )
    return goal_fn

goal_fn = make_goal_fn()

problem.add_actions([
    goal_fn
])


problem.add_fluents([
    function_count
])
problem.set_initial_value(function_count, 0)

px = Variable("px", Pixel)
problem.add_goal(
    And(
        Forall(occupied(px), px),
        GE(function_count, 5)
    )
)

print(problem)
to_pddl.export(problem, plibPath("benchmarks") / os.path.basename(__file__).strip(".py"))

with OneshotPlanner(name='enhsp') as planner:
    result = planner.solve(problem)
    plan = result.plan
    if plan is not None:
        print("%s returned:" % planner.name)
        print(plan)
        with SequentialSimulator(problem=problem) as sim:
            plan_goal_simulator.simulate(plan, sim, problem)
    else:
        print("No plan found.")
