import unified_planning
from unified_planning.shortcuts import *
from unified_planning.model.metrics import MinimizeSequentialPlanLength


Counter = UserType('Counter')

value = Fluent('value', IntType(), m=Counter)

inc = InstantaneousAction('increment',c=Counter)
c = inc.parameter('c')
inc.add_precondition(LE(value(c), 10))
inc.add_increase_effect(value(c), 1)

dec = InstantaneousAction('decrement',c=Counter)
c = dec.parameter('c')
dec.add_precondition(GT(value(c), 0))
dec.add_decrease_effect(value(c),1)


N = 9 # This is the number of counters

p2 = Problem('Large_problems')

p2.add_fluent(value, default_initial_value=0)
p2.add_objects([Object(f'c{i}',Counter) for i in range(N)])
p2.add_action(inc)
p2.add_action(dec)

for i in range(N-1):
    p2.add_goal(GE(value(p2.object(f'c{i+1}')),Plus(value(p2.object(f'c{i}')),1)))



N = 7 #This is the number of counters

mediumSizeProblem = Problem('Medium_sized_problem')

mediumSizeProblem.add_fluent(value, default_initial_value=0)
mediumSizeProblem.add_objects([Object(f'c{i}',Counter) for i in range(N)])
mediumSizeProblem.add_action(inc)
mediumSizeProblem.add_action(dec)
metric = MinimizeSequentialPlanLength()
mediumSizeProblem.add_quality_metric(metric)

for i in range(N-1):
    mediumSizeProblem.add_goal(GE(value(p2.object(f'c{i+1}')),Plus(value(p2.object(f'c{i}')),1)))

with OneshotPlanner(problem_kind=mediumSizeProblem.kind,optimality_guarantee=True) as planner:
    result = planner.solve(mediumSizeProblem)
    plan = result.plan
    if plan is not None:
        print("%s returned:" % planner.name)
        print(plan)
    else:
        print("No plan found.")