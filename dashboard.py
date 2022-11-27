from dash import Dash, dash_table
import pandas as pd
from collections import OrderedDict
from dash import Input, Output, callback
import dash_bootstrap_components as dbc
from dash import html

from pathlib import Path

from pydicer.utils import read_converted_data

working_directory = Path("/home/patrick/tcia_pancreas")

df_objects = read_converted_data(working_directory)

df_patients = df_objects[
    [
        "patient_id",
    ]
]
df_patients = df_patients.drop_duplicates()
df_patients = df_patients.sort_values("patient_id")

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        data=df_patients.to_dict("records"),
                        id="patients_table",
                        columns=[{"id": c, "name": c} for c in df_patients.columns],
                        style_as_list_view=True,
                        style_cell={"padding": "15px"},
                        style_header={"backgroundColor": "grey", "fontWeight": "bold"},
                        style_cell_conditional=[
                            {"if": {"column_id": c}, "textAlign": "left"}
                            for c in ["patient_id"]
                        ],
                        page_size=10,
                    )
                ),
                dbc.Col(
                    dash_table.DataTable(
                        data=df_objects.to_dict("records"),
                        id="objects_table",
                        columns=[
                            {"id": "modality", "name": "modality"},
                            {"id": "hashed_uid", "name": "hashed_uid"},
                        ],
                        style_as_list_view=True,
                        style_cell={"padding": "15px"},
                        style_header={"backgroundColor": "grey", "fontWeight": "bold"},
                        style_cell_conditional=[
                            {"if": {"column_id": c}, "textAlign": "left"}
                            for c in ["patient_id"]
                        ],
                    )
                ),
                dbc.Col(html.Div("this part is empty (sorry will do later)")),
            ]
        ),
        dbc.Alert(id="tbl_out"),
    ]
)


@callback(Output("objects_table", "data"), Input("patients_table", "active_cell"))
def update_graphs(active_cell):
    if active_cell is not None:
        patient_row = active_cell["row"]
        patient_id = df_patients.iloc[patient_row].patient_id

        return df_objects[df_objects.patient_id == patient_id].to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
