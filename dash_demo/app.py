import numpy
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc


def to_categorical(column, bin_size=5, min_cut=15, max_cut=50):
    if min_cut is None:
        min_cut = int(round(column.min())) - 1
    value_max = int(numpy.ceil(column.max()))
    max_cut = min(max_cut, value_max)
    intervals = [(x, x + bin_size) for x in range(min_cut, max_cut, bin_size)]
    if max_cut != value_max:
        intervals.append((max_cut, value_max))
    return pd.cut(column, pd.IntervalIndex.from_tuples(intervals))


url = 'https://www.famaf.unc.edu.ar/~nocampo043/sysarmy_survey_2020_processed.csv'
df = pd.read_csv(url)

df_fp = df[df["work_contract_type"].isin(["Full-Time", "Part-Time"])]

salary_vs_contract_sc_fig = px.scatter(df_fp,
                                       y="salary_monthly_GROSS",
                                       x="salary_monthly_NET",
                                       color="work_contract_type",
                                       color_discrete_sequence=["lightseagreen", "indianred"])

salary_vs_contract_sc_fig.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    font_color="white",
)

salary_vs_contract_box_fig = px.box(df_fp,
                                    x="work_contract_type",
                                    y="salary_monthly_NET",
                                    points="all", color_discrete_sequence=["lightseagreen"])

salary_vs_contract_box_fig.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    font_color="white",
    yaxis_range=[0,1000000]
)

# salary_vs_contract_box_fig.update_layout(height=700, width=900)

df_fp['profile_age_segment'] = to_categorical(df.profile_age)

df_age_segment_mean = (
    df_fp[["profile_age_segment", "salary_monthly_NET"]]
      .groupby("profile_age_segment")
      .agg(salary_monthly_NET_mean=("salary_monthly_NET", "mean"),
           salary_monthly_NET_std=("salary_monthly_NET", "std"))
      .reset_index()
)

df_age_segment_mean["profile_age_segment_str"] = df_age_segment_mean[
    "profile_age_segment"].astype(str)
salary_vs_age_bar_fig = px.bar(df_age_segment_mean,
                               x='profile_age_segment_str',
                               y='salary_monthly_NET_mean',
                               error_y="salary_monthly_NET_std",
                               color_discrete_sequence=["lightseagreen"])

salary_vs_age_bar_fig.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    font_color="white",
)

external_stylesheets = [{"href": "./assets/styles.css", "rel": "stylesheet"}]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    # Header
    html.Div(
        children=[
            # Title
            html.Div(children=[
                html.H1(children="Monthly Salary in Argentina - Survey Sysarmy"),
                html.
                P(children=
                  "Comparing salary monthly net and multiple variables",
                  className="header__title")
            ]),
            html.Img(src="./assets/dash-new-logo.png",
                     className="header__logo")
        ],
        className="header"),
    # Content
    html.Div(children=[
        html.Div(children=[dcc.Graph(figure=salary_vs_contract_box_fig, className="left_plot--graph")], className="left_plot column"),
        html.Div(children=[
            dcc.Graph(figure=salary_vs_contract_sc_fig),
            dcc.Graph(figure=salary_vs_age_bar_fig)
        ], className="right_plot column")
    ],
             className="content")
], className="container")

if __name__ == '__main__':
    app.run_server(debug=True)