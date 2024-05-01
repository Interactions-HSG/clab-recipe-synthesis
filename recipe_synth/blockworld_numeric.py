import pathlib

from unified_planning.shortcuts import (
    UserType,
    BoolType,
    IntType,
    GE,
    OneshotPlanner
)
from unified_planning.model import (
    Fluent,
    InstantaneousAction,
    Object,
    Problem
)

import to_pddl
## Types
# Type for gemoetrical shape
Shape = UserType("Shape")

# Type for inventory
Block = UserType(name="Block", father=Shape)
# Block = UserType(name="Block")

# # Type for the tower we want to build
Tower = UserType(name="Tower", father=Shape)

## Fluents == Predicates
# Shape independet
handemtpy = Fluent("handempty", BoolType())

# For all kinds of shapes
on = Fluent("on", BoolType(), sh_a=Shape, sh_b=Shape)
clear = Fluent("clear", BoolType(), sh_clear=Shape)
# Left-handed CD - gain orientation in frame without braking your fingers
size_y_of = Fluent("size_y_of", IntType(), sh_size=Shape)

# Block specific
ontable = Fluent("ontable", BoolType(), blk_ot=Block)
holding = Fluent("holding", BoolType(), blk_hold=Block) # You can hold the door but not the tower

# tower_y = Fluent("shape_y", IntType())


## Actions
pick_up_shape = InstantaneousAction("pick-up", blk=Block)
blk = pick_up_shape.parameter("blk")
pick_up_shape.add_precondition(ontable(blk))
pick_up_shape.add_precondition(handemtpy())
pick_up_shape.add_precondition(clear(blk))
pick_up_shape.add_effect(ontable(blk), False)
pick_up_shape.add_effect(clear(blk), False)
pick_up_shape.add_effect(holding(blk), True)
pick_up_shape.add_effect(handemtpy(), False)
# print(pick_up_shape)

put_down_shape = InstantaneousAction("put-down", blk=Block)
blk = put_down_shape.parameter("blk")
put_down_shape.add_precondition(holding(blk))
put_down_shape.add_effect(ontable(blk), True)
put_down_shape.add_effect(clear(blk), True)
put_down_shape.add_effect(holding(blk), False)
put_down_shape.add_effect(handemtpy(), True)
# print(put_down_shape)

attach_shape = InstantaneousAction("attach", blk=Block, sh_dst=Shape)
blk = attach_shape.parameter("blk")
sh_dst = attach_shape.parameter("sh_dst")
attach_shape.add_precondition(holding(blk))
attach_shape.add_precondition(clear(sh_dst))
attach_shape.add_effect(on(blk, sh_dst), True)
attach_shape.add_effect(holding(blk), False)
attach_shape.add_effect(handemtpy(), True)
attach_shape.add_effect(clear(blk), True)
attach_shape.add_effect(clear(sh_dst), False)
attach_shape.add_increase_effect(size_y_of(sh_dst), size_y_of(blk))
# print(attach_shape)

detach_shape = InstantaneousAction("detach", sh_from=Shape, blk=Block)
sh_from = detach_shape.parameter("sh_from")
blk = detach_shape.parameter("blk")
detach_shape.add_precondition(handemtpy())
detach_shape.add_precondition(clear(sh_from))
detach_shape.add_precondition(GE(size_y_of(sh_from), size_y_of(blk)))
detach_shape.add_effect(on(blk, sh_from), False)
detach_shape.add_effect(holding(blk), True)
detach_shape.add_effect(handemtpy(), False)
detach_shape.add_effect(clear(blk), False)
detach_shape.add_effect(clear(sh_from), True)
detach_shape.add_decrease_effect(size_y_of(sh_from), size_y_of(blk))
# print(detach_shape)

problem = Problem("problem")

problem.add_fluent(on, default_initial_value=False)
problem.add_fluent(ontable, default_initial_value=True)
problem.add_fluent(clear, default_initial_value=True)
problem.add_fluent(handemtpy, default_initial_value=True)
problem.add_fluent(holding, default_initial_value=False)
problem.add_fluent(size_y_of, default_initial_value=0)


problem.add_actions([
    pick_up_shape, put_down_shape, attach_shape, detach_shape
])

blk_ids = ["A", "B", "C"]
blks = [Object(f"{id}", Block) for id in blk_ids]
problem.add_objects(blks)

for blk in blks:
    problem.set_initial_value(size_y_of(blk), 1)
    problem.set_initial_value(ontable(blk), True)
    problem.set_initial_value(clear(blk), True)


tower = Object("tower", Tower)
problem.add_object(tower)
problem.set_initial_value(size_y_of(tower), 0)
problem.set_initial_value(clear(tower), True)
# problem.set_initial_value(ontable(tower), False)

problem.add_goal(GE (size_y_of(tower),3))

print(problem)
to_pddl.export(problem, pathlib.Path("benchmarks") / "blocks_numeric")


# with OneshotPlanner(problem_kind=problem.kind) as planner:
#     result = planner.solve(problem)
#     if result.plan is not None:
#         print("%s returned:" % planner.name)
#         print(result.plan)
#     else:
#         print("No plan found.")
