import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from dash import Dash
from dash import dcc
from dash import html

url = 'https://www.famaf.unc.edu.ar/~nocampo043/sysarmy_survey_2020_processed.csv'
df = pd.read_csv(url)

sorted_studies_levels = ["Primary", "Secondary", "Terciary", "University",
                         "Postgraduate", "Doctorate", "Postdoc"]

# Barplot of the profile_studies_level alongside their frequency count.
df_studies_level_count = (
    df["profile_studies_level"]
      .value_counts()
      .reset_index()
      .rename(columns={"index": "profile_studies_level",
                       "profile_studies_level": "count"})
)

studies_level_count_fig = px.bar(df_studies_level_count,
                                 x='profile_studies_level',
                                 y='count',
                                 category_orders=dict(profile_studies_level=sorted_studies_levels))

# Barplot of the profile_studies_level alongside the mean of the salary

df_studies_level_mean = (
    df[["profile_studies_level", "salary_monthly_NET"]]
      .groupby("profile_studies_level")
      .mean()
      .reset_index()
      .rename(columns={"salary_monthly_NET": "salary_monthly_NET_mean"})
)

studies_level_mean_fig = px.bar(df_studies_level_mean,
                                x='profile_studies_level',
                                y='salary_monthly_NET_mean',
                                category_orders=dict(profile_studies_level=sorted_studies_levels))


# Barplot using grouped studies level alongside the mean of the salary
new_groups = {
    'Postdoc': 'Postgraduate',
    'Doctorate': 'Postgraduate',
    'Primary': 'Pre-degree',
    'Secondary': 'Pre-degree'
}
order = ['Pre-degree', 'Terciary', 'University', 'Postgraduate']
grouped_studies_level = df.profile_studies_level.replace(new_groups)
df["grouped_profile_studies_level"] = grouped_studies_level

df_grouped_studies_level_mean = (
    df[["grouped_profile_studies_level", "profile_studies_level_state", "salary_monthly_NET"]]
      .groupby(["grouped_profile_studies_level", "profile_studies_level_state"])
      .mean()
      .reset_index()
      .rename(columns={"salary_monthly_NET": "salary_monthly_NET_mean"})
)

grouped_studies_level_fig = px.bar(df_grouped_studies_level_mean,
                                   x='grouped_profile_studies_level',
                                   y='salary_monthly_NET_mean',
                                   color='profile_studies_level_state',
                                   barmode='group',
                                   category_orders=dict(grouped_profile_studies_level=order))

header = {
    "background-color": "#222222",
    "height": "256px",
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "center;",
}

header_title = {
    'color': '#FFFFFF',
    'font-size': '48px',
    'font-weight': 'bold',
    'text-align': 'center',
    'margin': '0 auto',
}

header_description = {
    'color': '#CFCFCF',
    'margin': '4px auto',
    'text-align': 'center',
    'max-width': '384px',
}

plot_card = {
    'margin-bottom': '24px',
    'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'
}

wrapper = {
    'margin-right': 'auto',
    'margin-left': 'auto',
    'max-width': '1024px',
    'padding-right': '10px',
    'padding-left': '10px',
    'margin-top': '32px',
    'font-family': '"Lato", sans-serif',
    'background-color': '#F7F7F7'
}

app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Using Dash", style=header_title),
                html.P(
                    children="Analyze the salary monthly net alongside the years of experience",
                    style=header_description
                )     
            ],
            style=header),
        html.Div(
            children=[
                dcc.Graph(figure=studies_level_count_fig),
                dcc.Graph(figure=studies_level_mean_fig),
                dcc.Graph(figure=grouped_studies_level_fig)         
            ],
            style=plot_card,
        )
    ],
    style=wrapper
)

if __name__ =='__main__':
    app.run_server(debug=True)