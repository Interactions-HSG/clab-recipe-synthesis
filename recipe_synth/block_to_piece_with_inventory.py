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
# Crutch to make objects id-able
IDableType = UserType("IDableType")
type2id = Fluent("type2id", IntType(), id=IDableType)

PieceType = UserType('PieceType', father=IDableType)
piece_dim = Fluent('piece_dim', IntType(), p=PieceType)

BlockType = UserType("BlockType", father=IDableType)
block_dim = Fluent("block_dim", IntType(), b=BlockType)

# Mapping function to mock a fabric block with different values in each dimension
block_size = Fluent("block_size", IntType(), sid=BlockType)

inc = InstantaneousAction(
    'increment',
    c=PieceType,
    blk=BlockType
)
c = inc.parameter('c')
blk = inc.parameter('blk')
# there is at least one fabric block left in the inventory
inc.add_precondition(GE(block_dim(blk), 1))
# Stay within the boundaries of the desired piece
inc.add_precondition(LE(piece_dim(c), 10))
inc.add_precondition(Equals(type2id(c), type2id(blk)))
inc.add_increase_effect(piece_dim(c), block_size(blk)) # the piece grows ...
inc.add_decrease_effect(block_dim(blk), 1) # ... but our inventory shrinks

dec = InstantaneousAction(
    'decrement',
    c=PieceType,
    blk=BlockType
)
c = dec.parameter('c')
blk = inc.parameter('blk')
# fabric blocks cannot be created hence shall not exceed there initial value
# this is not implemented correctly yet
dec.add_precondition(LE(block_dim(blk), 6))
# fabric blocks cannot be removed if there is nothing left to be removed from
dec.add_precondition(GT(piece_dim(c), 0))
# 
inc.add_precondition(Equals(type2id(c), type2id(blk)))
dec.add_decrease_effect(piece_dim(c), block_size(blk))
dec.add_increase_effect(block_dim(blk), 1)

problem = Problem('CounterWithInventory')

problem.add_fluent(piece_dim, default_initial_value=0)
problem.add_fluent(block_dim, default_initial_value=0)
problem.add_fluent(block_size, default_initial_value=0)
problem.add_fluent(type2id, default_initial_value=0)

domain_objects_names = []
domain_objects = {}

NOBJ = 3
TERMGOAL = "piece_dim"
TERMELEM = "fabric_block_dim"
for id in range(NOBJ):
    domain_objects_names.append(f"{TERMGOAL}{id}")
    domain_objects_names.append(f"{TERMELEM}{id}")
for dobjn in domain_objects_names:
    if dobjn.startswith(TERMELEM):
        domain_objects.update({dobjn: Object(dobjn, BlockType)})
    elif dobjn.startswith(TERMGOAL):
        domain_objects.update({dobjn: Object(dobjn, PieceType)})
problem.add_objects(domain_objects.values())

for obj_id in range(NOBJ):
    problem.set_initial_value(block_size(domain_objects[f"{TERMELEM}{obj_id}"]), obj_id)
    problem.set_initial_value(type2id(domain_objects[f"{TERMELEM}{obj_id}"]), obj_id)
    problem.set_initial_value(type2id(domain_objects[f"{TERMGOAL}{obj_id}"]), obj_id)
# Not looped since they shall have different values
problem.set_initial_value(block_dim(domain_objects[f"{TERMELEM}0"]), 5) 
problem.set_initial_value(block_dim(domain_objects[f"{TERMELEM}1"]), 4) 
problem.set_initial_value(block_dim(domain_objects[f"{TERMELEM}2"]), 3) 

problem.add_action(inc)
problem.add_action(dec)

problem.add_goal(GE(
    Plus(
        Plus(piece_dim(domain_objects[f"{TERMGOAL}0"]), piece_dim(domain_objects[f"{TERMGOAL}1"])),
        piece_dim(domain_objects[f"{TERMGOAL}2"])), 10)
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
