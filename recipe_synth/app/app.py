from pathlib import Path

import dash
from dash import html, dcc
from dash.long_callback import DiskcacheLongCallbackManager, DiskcacheManager
import diskcache

from recipe_synth.app import callbacks


class RecipeSynthesizer():
    # TODO: Makes this a dash page instead
    # https://dash.plotly.com/urls
    _app = None
    _planner = None
    _layout = None

    @property
    def layout(self):
        return self._layout

    def __init__(self, app) -> None:
        self._app = app
        self.make_layout()
        # Callbacks need background_callback_manager. Error message by Dash should be enough
        callbacks.get_callbacks(self._app)

    def make_layout(self):

        # Function to read Markdown content from a file
        def read_markdown_file(filename):
            folder_path = Path(__file__).resolve().parent.parent.parent # Path to subfolder parallel to parent folder
            file_path = folder_path / filename
            with open(file_path, 'r') as file:
                markdown_content = file.read()
            return markdown_content
        
        # Ugly way of splitting the sections of the markdown file
        # TODO: find a regex to do this nice. Parsers seem over kill.
        mdfile = read_markdown_file("README.md")
        sec_main = mdfile.partition("### Planner Result")
        sec_legend = sec_main[2].partition("### Legend")
        sec_legend = sec_legend[1] + sec_legend[2].split("### Discussion")[0]
        sec_discussion = sec_main[2].partition("### Discussion")
        sec_discussion = sec_discussion[1] + sec_discussion[2]
        
        self._layout = html.Div(
            [
                html.Div([dcc.Markdown(children=sec_main[0])]),
                html.Div([dcc.Markdown(children=sec_legend)]),
                html.Button("Submit", id="button"),
                html.Button("Cancel", id="cancel_button", disabled=True),
                html.Div(children="live updated", id="update-output"),
                html.Div(children="waiting for plan", id="planner-output"),
                html.Div([dcc.Markdown(children=sec_discussion)]),
            ],
        )
        self._app.layout = self._layout

if __name__ == '__main__':
    # TODO: Move this to OS specific caches
    cache = diskcache.Cache(Path(__file__).parent / "cache")
    background_callback_manager = DiskcacheManager(cache)

    app = dash.Dash(__name__, background_callback_manager=background_callback_manager)
    planner = RecipeSynthesizer(app)

    app.run_server(debug=True)