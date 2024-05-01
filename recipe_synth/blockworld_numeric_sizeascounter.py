import pathlib

from unified_planning.shortcuts import (
    UserType,
    BoolType,
    IntType,
    GE,
    LE,
    Equals,
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
# Shape = UserType("Shape")

# Type for inventory
# Block = UserType(name="Block", father=Shape)
Block = UserType(name="Block")
Size = UserType("Size")

# # Type for the tower we want to build
# Tower = UserType(name="Tower", father=Shape)

## Fluents == Predicates
# Shape independet
handemtpy = Fluent("handempty", BoolType())

# For all kinds of shapes
on = Fluent("on", BoolType(), x=Block, y=Block)
clear = Fluent("clear", BoolType(), x=Block)
# Left-handed CD - gain orientation in frame without braking your fingers
# We are using a counter here instead of a target shape
# size_y = Fluent("size_y", IntType(), s=Size)
size_y = Fluent("size_y", IntType())
size_block = Fluent("size_block", IntType(), x=Block)

# Block specific
ontable = Fluent("ontable", BoolType(), x=Block)
holding = Fluent("holding", BoolType(), x=Block) # You can hold the door but not the tower

# tower_y = Fluent("shape_y", IntType())


## Actions
pick_up_shape = InstantaneousAction("pick-up", x=Block)
x = pick_up_shape.parameter("x")
pick_up_shape.add_precondition(ontable(x))
pick_up_shape.add_precondition(handemtpy())
pick_up_shape.add_precondition(clear(x))
pick_up_shape.add_effect(ontable(x), False)
pick_up_shape.add_effect(clear(x), False)
pick_up_shape.add_effect(holding(x), True)
pick_up_shape.add_effect(handemtpy(), False)
# print(pick_up_shape)

put_down_shape = InstantaneousAction("put-down", x=Block)
x = put_down_shape.parameter("x")
put_down_shape.add_precondition(holding(x))
put_down_shape.add_effect(ontable(x), True)
put_down_shape.add_effect(clear(x), True)
put_down_shape.add_effect(holding(x), False)
put_down_shape.add_effect(handemtpy(), True)
# print(put_down_shape)

attach_shape = InstantaneousAction("attach", x=Block, y=Block)
x = attach_shape.parameter("x")
y = attach_shape.parameter("y")
attach_shape.add_precondition(holding(x))
attach_shape.add_precondition(clear(y))
attach_shape.add_effect(on(x, y), True)
attach_shape.add_effect(holding(x), False)
attach_shape.add_effect(handemtpy(), True)
attach_shape.add_effect(clear(x), True)
attach_shape.add_effect(clear(y), False)
attach_shape.add_increase_effect(size_y(), size_block(x))
# print(attach_shape)

detach_shape = InstantaneousAction("detach", x=Block, y=Block)
x = detach_shape.parameter("x")
y = detach_shape.parameter("y")
detach_shape.add_precondition(handemtpy())
detach_shape.add_precondition(clear(x))
detach_shape.add_precondition(GE(size_y(), size_block(x)))
detach_shape.add_effect(on(x, y), False)
detach_shape.add_effect(holding(x), True)
detach_shape.add_effect(handemtpy(), False)
detach_shape.add_effect(clear(x), False)
detach_shape.add_effect(clear(y), True)
detach_shape.add_decrease_effect(size_y(), size_block(x))
# print(detach_shape)

problem = Problem("problem")

problem.add_fluent(on, default_initial_value=False)
problem.add_fluent(ontable, default_initial_value=True)
problem.add_fluent(clear, default_initial_value=True)
problem.add_fluent(handemtpy, default_initial_value=True)
problem.add_fluent(holding, default_initial_value=False)
problem.add_fluent(size_y, default_initial_value=0)
problem.add_fluent(size_block, default_initial_value=0)


problem.add_actions([
    pick_up_shape, put_down_shape, attach_shape#, detach_shape
])

blk_ids = ["A", "B", "C"]
blks = [Object(f"{id}", Block) for id in blk_ids]
problem.add_objects(blks)

for blk in blks:
    problem.set_initial_value(size_block(blk), 1)
    problem.set_initial_value(ontable(blk), True)
    problem.set_initial_value(clear(blk), True)


# tower = Object("tower", Block)
# problem.add_object(tower)
# problem.set_initial_value(size_y_of(tower), 0)
# problem.set_initial_value(clear(tower), True)
# problem.set_initial_value(ontable(tower), False)

problem.add_goal(Equals(size_y(),3))
# problem.add_goal(GE (size_y_of(tower),3))
# problem.add_goal(LE (size_y_of(tower),4))

print(problem)
to_pddl.export(problem, pathlib.Path("benchmarks") / "blocks_numeric")


with OneshotPlanner(problem_kind=problem.kind) as planner:
    result = planner.solve(problem)
    if result.plan is not None:
        print("%s returned:" % planner.name)
        print(result.plan)
    else:
        print("No plan found.")
