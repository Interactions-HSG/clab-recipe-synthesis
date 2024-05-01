import os.path

import unified_planning
from unified_planning.shortcuts import *
from unified_planning.model.metrics import MinimizeSequentialPlanLength

import to_pddl


"""
s_id("s1") = 2 
c_id("c2") = 2
and(c_id, s_sid) == True
stock_2_inc(s_sid) = 1.5
"""
IDableType = UserType("IDableType")
id = Fluent("id", BoolType(), id=IDableType)

CounterType = UserType('CounterType', father=IDableType)
c_value = Fluent('c_value', IntType(), m=CounterType)

IncrementalType = UserType("IncrementalType")
inc_value = Fluent("inc_value", IntType(), ic=IncrementalType)

StockType = UserType("StockType", father=IDableType)
stock_value = Fluent("stock_value", IntType(), s=StockType)

IncrementStockMappingType = BoolType()
# inc_2_stock = UserType("inc_2_stock", BoolType(), ism=IncrementStockMappingType)
# inc_2_stock = Fluent("inc_2_stock", BoolType(), cid=CounterType, sid=StockType)
stock_2_inc = Fluent("stock_2_inc", IntType(), sid=StockType)

counter2stock = Fluent("counter2stock", IntType(), cid=CounterType)



# inc = InstantaneousAction('increment',c=Counter)
# c = inc.parameter('c')
# inc.add_precondition(LE(value(c), 10))
# inc.add_increase_effect(value(c), 1)
inc = InstantaneousAction(
    'increment',
    c=CounterType,
    ic=IncrementalType, # get rid of this - inc is determined by s_id and c_id
    blk=StockType
    # ,ism=IncrementStockMappingType
)
c = inc.parameter('c')
ic = inc.parameter('ic')
blk = inc.parameter('blk')
# ism = inc.parameter("ism")
# inc.add_precondition(GE(stock_value(blk), 1))
inc.add_precondition(LE(c_value(c), 10))
# inc.add_precondition(Equals(inc_2_stock(blk)))
inc.add_increase_effect(c_value(c), inc_value(ic))
# inc.add_decrease_effect(stock_value(blk), 1)

# dec = InstantaneousAction('decrement',c=Counter)
# c = dec.parameter('c')
# dec.add_precondition(GT(value(c), 0))
# dec.add_decrease_effect(value(c),1)
dec = InstantaneousAction('decrement',c=CounterType, ic=IncrementalType, blk=StockType)
c = dec.parameter('c')
ic = inc.parameter('ic')
blk = inc.parameter('blk')
# inc.add_precondition(LE(stock_value(blk), 6))
dec.add_precondition(GT(c_value(c), 0))
dec.add_decrease_effect(c_value(c), inc_value(ic))
# dec.add_increase_effect(stock_value(blk), 1)

problem = Problem('CounterWithInventory')

problem.add_fluent(c_value, default_initial_value=0)
problem.add_fluent(inc_value, default_initial_value=1)
# problem.add_fluent(stock_value, default_initial_value=0)
problem.add_fluent(stock_2_inc, default_initial_value=0)

domain_objects_names = []
domain_objects = {}


for id in range(3):
    domain_objects_names.append(f"c{id}")
    domain_objects_names.append(f"stock{id}")

for dobjn in domain_objects_names:
    if dobjn.startswith("stock"):
        domain_objects.update({dobjn: Object(dobjn, StockType)})
    elif dobjn.startswith("c"):
        domain_objects.update({dobjn: Object(dobjn, CounterType)})
    # creat IDs for stock and counter

I = Object("inc", IncrementalType)
domain_objects.update({I.name: I})
problem.add_objects(domain_objects.values())

problem.add_action(inc)
problem.add_action(dec)
problem.set_initial_value(inc_value(I), 1)
problem.set_initial_value(stock_2_inc(domain_objects["stock0"]), 0)
# problem.add_goal(And( GE(value(C2),Plus(value(C1),1)), GE(value(C1),Plus(value(C0),1))))
problem.add_goal(GE(Plus(
    Plus(c_value(domain_objects["c0"]),c_value(domain_objects["c1"])),c_value(domain_objects["c2"])), 18))
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