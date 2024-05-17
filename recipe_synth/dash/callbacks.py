from dash import html, dcc
from dash.dependencies import Input, Output
from unified_planning.shortcuts import SequentialSimulator

from recipe_synth import block_to_piece, plan_goal_simulator

def get_callbacks(app):
    @app.long_callback(
    [
        Output("planner-output", "children"),
    ],
    Input("button", "n_clicks"),
    running=[
        (Output("button", "disabled"), True, False),
        (Output("cancel_button", "disabled"), False, True),
    ],
    cancel=[Input("cancel_button", "n_clicks")],
    progress=[Output("update-output", "children")],
    prevent_initial_call=True
    )
    def change_text(
        set_progress,
        n_clicks
        ):
        set_progress(["planning..."])
        problem, plan = block_to_piece.run_planner(should_run_simulation=False)
        if plan:
            with SequentialSimulator(problem=problem) as sim:
                df = plan_goal_simulator.simulate_b2p(plan, sim, problem)
        
        set_progress(["Sequential plan:"])
        return [html.Div([dcc.Markdown(children=df.to_markdown())])]