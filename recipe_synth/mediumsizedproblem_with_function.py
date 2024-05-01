import os.path

import unified_planning
from unified_planning.shortcuts import *
from unified_planning.model.metrics import MinimizeSequentialPlanLength

import to_pddl

Counter = UserType('Counter')

value = Fluent('value', IntType(), m=Counter)

Incremental = UserType("Incremental")

inc_value = Fluent("inc_value", IntType(), ic=Incremental)

# inc = InstantaneousAction('increment',c=Counter)
# c = inc.parameter('c')
# inc.add_precondition(LE(value(c), 10))
# inc.add_increase_effect(value(c), 1)
inc = InstantaneousAction('increment',c=Counter, ic=Incremental)
c = inc.parameter('c')
ic = inc.parameter('ic')
inc.add_precondition(LE(value(c), 5))
inc.add_increase_effect(value(c), inc_value(ic))

# dec = InstantaneousAction('decrement',c=Counter)
# c = dec.parameter('c')
# dec.add_precondition(GT(value(c), 0))
# dec.add_decrease_effect(value(c),1)
dec = InstantaneousAction('decrement',c=Counter, ic=Incremental)
c = dec.parameter('c')
ic = inc.parameter('ic')
dec.add_precondition(GT(value(c), 0))
dec.add_decrease_effect(value(c), inc_value(ic))

problem = Problem('problem')

problem.add_fluent(value, default_initial_value=0)
problem.add_fluent(inc_value, default_initial_value=1)
C0 = Object('c0', Counter)
C1 = Object('c1', Counter)
C2 = Object('c2', Counter)
I = Object("inc", Incremental)
problem.add_object(C0)
problem.add_object(C1)
problem.add_object(C2)
problem.add_object(I)
problem.add_action(inc)
problem.add_action(dec)
problem.set_initial_value(inc_value(I), 1)
# problem.add_goal(And( GE(value(C2),Plus(value(C1),1)), GE(value(C1),Plus(value(C0),1))))
problem.add_goal(GE(Plus(Plus(value(C1),value(C2)),value(C0)), 18))
print(problem)

to_pddl.export(problem, os.path.basename(__file__).strip(".py"))

with OneshotPlanner(name='enhsp') as planner:
    result = planner.solve(problem)
    plan = result.plan
    if plan is not None:
        print("%s returned:" % planner.name)
        print(plan)
    else:
        print("No plan found.")