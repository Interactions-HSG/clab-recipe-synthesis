from pathlib import Path

from unified_planning.io.pddl_writer import PDDLWriter


def export(problem, path: Path):
    w = PDDLWriter(problem)
    path_base = Path(__file__).parent
    path_dst = path_base / path
    path_dst.mkdir(parents=True, exist_ok=True)
    w.write_domain(path_dst / 'domain.pddl')
    w.write_problem(path_dst / 'problem.pddl')