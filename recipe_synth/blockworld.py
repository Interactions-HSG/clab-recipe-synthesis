import os
from pathlib import Path

from unified_planning.io import PDDLReader
from unified_planning.shortcuts import Problem, OneshotPlanner

import to_pddl

reader = PDDLReader()
path = Path(__file__).parent / "benchmarks" / "blocks"
pddl_problem = reader.parse_problem(path / "domain.pddl", path / "task01.pddl")
print(pddl_problem)

to_pddl.export(pddl_problem, os.path.basename(__file__).strip(".py"))

with OneshotPlanner(problem_kind=pddl_problem.kind) as planner:
    result = planner.solve(pddl_problem)
    if result.plan is not None:
        print("%s returned:" % planner.name)
        print(result.plan)
    else:
        print("No plan found.")
