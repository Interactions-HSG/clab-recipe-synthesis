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
ShapeType = UserType("ShapeType")
BlockVarType = UserType("BlockVarType", father=ShapeType)
BlockInvType = UserType("BlockInvType")
PieceType = UserType('PieceType', father=ShapeType)

dim_x = Fluent("dim_x", IntType(), dimx=ShapeType)
dim_y = Fluent("dim_y", IntType(), dimy=ShapeType)
block_inv = Fluent("block_inv", IntType(), blk=BlockVarType)



inc_x = InstantaneousAction(
    'attach_x',
    blk=BlockVarType,
    p=PieceType
)
blk = inc_x.parameter('blk')
p = inc_x.parameter('p')
# there is at least one fabric block left in the inventory
inc_x.add_precondition(GE(block_inv(blk), 1))
inc_x.add_increase_effect(dim_x(p), dim_x(blk)) # the piece grows in x ...
inc_x.add_increase_effect(dim_y(p), dim_y(blk), Equals(0,dim_y(p))) # and y but only if it is the first block
inc_x.add_decrease_effect(block_inv(blk), 1) # ... but our inventory shrinks

inc_y = InstantaneousAction(
    'attach_y',
    blk=BlockVarType,
    p=PieceType
)
blk = inc_y.parameter('blk')
p = inc_y.parameter('p')
# there is at least one fabric block left in the inventory
inc_y.add_precondition(GE(block_inv(blk), 1))
inc_y.add_increase_effect(dim_x(p), dim_x(blk)) # the piece grows in y ...
inc_y.add_increase_effect(dim_x(p), dim_x(blk), Equals(0,dim_x(p))) # and x but only if it is the first block
inc_y.add_decrease_effect(block_inv(blk), 1) # ... but our inventory shrinks

problem = Problem('BlockToPieceWithInventory')

problem.add_fluents([
    dim_x, dim_y, block_inv
])

# Needed objects
# 2x Blocks of variant 1
# 1x Block of variant 2
# 1x Piece
NBLOCKSVAR1 = 2
NBLOCKSVAR2 = 1
NVARS = 2
BLOCKNAME = "BlockVar"
INVNAME = "BlockInv"

domain_objects_names = []
domain_objects = {}

# for var in range(NVARS):
#     for num in range(NBLOCKSVAR1):
#         name = f"{BLOCKNAME}_{var}_{num}"
#         domain_objects.update({name: Object(name, BlockVarType)})
#         dobj = problem.add_object(f"{BLOCKNAME}_{var}_{num}", BlockVarType)
#         if 0 == var:
#             problem.set_initial_value(dim_x(dobj), 1)
#             problem.set_initial_value(dim_y(dobj), 1)
#             problem.set_initial_value(block_inv(dobj), NBLOCKSVAR1)
#         elif 1 == var:
#             problem.set_initial_value(dim_x(dobj), 2)
#             problem.set_initial_value(dim_y(dobj), 1)
#             problem.set_initial_value(block_inv(dobj), NBLOCKSVAR2)
blkvar1 = problem.add_object(f"{BLOCKNAME}_{1}", BlockVarType)
problem.set_initial_value(dim_x(blkvar1),1)
problem.set_initial_value(dim_y(blkvar1),1)
problem.add_object(f"{INVNAME}_{1}", BlockInvType)
problem.set_initial_value(block_inv(blkvar1), 2)

blkvar2 = problem.add_object(f"{BLOCKNAME}_{2}", BlockVarType)
problem.set_initial_value(dim_x(blkvar2),1)
problem.set_initial_value(dim_y(blkvar2),2)
problem.add_object(f"{INVNAME}_{2}", BlockInvType)
problem.set_initial_value(block_inv(blkvar2), 1)

p = problem.add_object("Piece", PieceType)
problem.set_initial_value(dim_x(p), 0)
problem.set_initial_value(dim_y(p), 0)

# pcur = problem.add_object("PieceCurrent", PieceCurrentType)
# problem.set_initial_value(dim_x(pcur), 0)
# problem.set_initial_value(dim_y(pcur), 0)

problem.add_action(inc_x)
problem.add_action(inc_y)

problem.add_goal(
    And(
        Equals(dim_x(p), 2),
        Equals(dim_y(p), 2)
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
            plan_goal_simulator.simulate_fb(plan, sim, problem)
    else:
        print("No plan found.")
