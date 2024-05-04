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


# In this mock, the pixel shape perfectly fit our desired piece
Pixel = UserType("Pixel")
pos_x = Fluent("pos_x", IntType(), s=Pixel)
problem.add_fluent(pos_x, default_initial_value=0)
pos_y = Fluent("pos_y", IntType(), s=Pixel)
problem.add_fluent(pos_y, default_initial_value=0)
domain_obj_names = []
domain_objs = {}
# pixel_objs = {}
for px_x in range(NPIXEL_X):
    for px_y in range(NPIXEL_Y):
        name = f"px_{px_x}_{px_y}"
        domain_obj_names.append(name)
        obj = problem.add_object(name, Pixel)
        domain_objs.update({name: obj})
        # pixel_objs.update({name: obj})
        problem.set_initial_value(pos_x(obj), px_x)
        problem.set_initial_value(pos_y(obj), px_y)

occupied = Fluent("occupied", BoolType(), s=Pixel)
problem.add_fluent(occupied, default_initial_value=False)

## Objects to model different block variants
BlockVarType = UserType("BlockVarType")
block_1_obj = Object("BlockVar_1", BlockVarType)
problem.add_object(block_1_obj)

## Each block has size in x and y that determines how many pixels are covered
block_size_x = Fluent("block_size_x", IntType(), blk=BlockVarType)
problem.add_fluent(block_size_x, default_initial_value=1)
problem.set_initial_value(block_size_x(block_1_obj), 1)

block_size_y = Fluent("block_size_y", IntType(), blk=BlockVarType)
problem.add_fluent(block_size_y, default_initial_value=1)
problem.set_initial_value(block_size_y(block_1_obj), 1)

block_2_obj = Object("BlockVar_2", BlockVarType)
problem.add_object(block_2_obj)
problem.set_initial_value(block_size_x(block_2_obj), 3)
problem.set_initial_value(block_size_y(block_2_obj), 1)

## Blocks have different stocks
BlockInvType = UserType("BlockInvType")
block_inv = Fluent("block_inv", IntType(), blk=BlockVarType)
problem.add_fluent(block_inv, default_initial_value=0)
problem.set_initial_value(block_inv(block_1_obj), 2)
problem.set_initial_value(block_inv(block_2_obj), 1)

# For informational and utility purposes only - not relevant for the problem
## Used to keep track of which block is used in a given pixel 
occupied_by = Fluent("occupied_by", IntType(), px=Pixel)
problem.add_fluent(occupied_by, default_initial_value=0)

## IDs the blocks
id_of = Fluent("id_of", IntType(), blk=BlockVarType)
problem.add_fluent(id_of)
problem.set_initial_value(id_of(block_1_obj), 1)
problem.set_initial_value(id_of(block_2_obj), 2)

## Used to store ints in case of swapping values of two fluents
int_buffer = Fluent("int_buffer", IntType())
problem.add_fluent(int_buffer, default_initial_value=0)
problem.set_initial_value(int_buffer,0)

## Utility fluent to be used e.g. in a goal to enforce function
function_count = Fluent("function_count", IntType())
problem.add_fluent(function_count)
problem.set_initial_value(function_count, 0)

def make_attach_fn(count=0):
    attach = InstantaneousAction(
        "attach",
        blk=BlockVarType,
        start_px=Pixel
    )
    blk = attach.parameter("blk")
    start_px = attach.parameter("start_px")
    attach.add_precondition(GE(block_inv(blk), 1)) # it must be 1 _before_ action
    # utility effect to force (one) function to get called
    if count:
        attach.add_increase_effect(function_count, count)
    p = Variable("p", Pixel)

    cond = And(
        GE( # definition to make effect easier: occupy only pixels larger than start
            pos_x(p),
            pos_x(start_px)
        ),
        LE( # limit the extend of the effect to size of the block
            pos_x(p),
            pos_x(start_px) + block_size_x(blk)
        ),
        GE( # definition to make effect easier: occupy only pixels larger than start
            pos_y(p),
            pos_y(start_px)
        ),
        LE( # limit the extend of the effect to size of the block
            pos_y(p),
            pos_y(start_px) + block_size_y(blk)
        )
    )
    # attaching a block makes the pixel that are within size occupied
    attach.add_effect(
        occupied(p),
        True,
        forall=(p,),
        condition=cond
    )
    # For visualization, we want to keep track of which block covers which pixel
    attach.add_effect(
        occupied_by(p),
        id_of(blk),
        forall=(p,),
        condition=cond
    )
    attach.add_decrease_effect(block_inv(blk), 1)

    return attach

def make_rotate_fn(count=0):
    rotate = InstantaneousAction(
        "rotate",
        blk=BlockVarType,
    )
    blk = rotate.parameter("blk")
    if count:
        rotate.add_increase_effect(function_count, count)
    # buffer the value before swapping - not sure if a planner would handle this by itself
    # However, unclear if effects are guaranteed to happen in order
    rotate.add_effect(int_buffer, block_size_x(blk))
    rotate.add_effect(block_size_x(blk), block_size_y(blk))
    rotate.add_effect(block_size_y(blk), int_buffer)

    return rotate

problem.add_actions([
    make_attach_fn(1),
    make_rotate_fn(0)
])

px = Variable("px", Pixel)
problem.add_goal(
    And(
        Forall(occupied(px), px),
        GE(function_count, 1)
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
            plan_goal_simulator.simulate_b2p(plan, sim, problem)
    else:
        print("No plan found.")
