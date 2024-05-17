from pathlib import Path

import dash
from dash import html
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache

from recipe_synth.dash import callbacks

def make_app(app):
    app.layout = html.Div(
        [
            html.Button("Submit", id="button"),
            html.Button("Cancel", id="cancel_button", disabled=True),
            html.Div(children="live updated", id="update-output"),
            html.Div(children="wait for final output", id="final-output"),
        ],
    )

if __name__ == '__main__':
    # TODO: Move this to OS specific caches
    cache = diskcache.Cache(Path(__file__).parent / "cache")
    long_callback_manager = DiskcacheLongCallbackManager(cache)

    app = dash.Dash(__name__, long_callback_manager=long_callback_manager)
    make_app(app)
    callbacks.get_callbacks(app)
    app.run_server(debug=True)