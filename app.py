import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

df = pd.read_csv(r"C:\Users\SHREYANSH SANKLECHA\OneDrive\Desktop\programmer's notes\Dash\dash_env\venv\Electric_Vehicle_Population_Data.csv")

app = Dash(__name__)

# EV Adoption Over Time
model_years = df["Model Year"].value_counts().sort_index()
fig1 = px.line(model_years, x = model_years.index, y = model_years.values, title = "I : EV Adoption Over Time")

# Selecting the top 3 counties based on EV registrations and then analyze the distribution of EVs within the cities of those counties
top_3_counties = df["County"].value_counts()[:3].index
data_of_top_counties = df[df["County"].isin(top_3_counties)]
top_cities = data_of_top_counties.groupby(["County","City"]).size().sort_values(ascending = False).reset_index(name='Number of Vehicles')[:10]
fig2 = px.bar(top_cities, x = 'Number of Vehicles', y = 'City', color = "County", color_discrete_sequence=px.colors.sequential.Magma, title = "II : Top Cities in Top Counties by EV Registrations")

# Let’s explore the types of electric vehicles represented in this dataset.
ev_type_dist = df["Electric Vehicle Type"].value_counts()
fig3 = px.bar(x = ev_type_dist.values, y = ev_type_dist.index, title = "III : Types of electric vehicles represented in this dataset")

# Let’s now focus on the popularity of electric vehicle manufacturers 
top_manuf = df["Make"].value_counts()[:10]
fig4 = px.bar(x = top_manuf.values, y = top_manuf.index, title = "IV : Popularity of electric vehicle Manufacturers")

# Popularity of electric vehicle Models
top_models = df["Model"].value_counts()[:10]
fig5 = fig5 = px.bar(x=top_models.values, y=top_models.index, title="V : Popularity of Electric Vehicle Models", color_discrete_sequence=px.colors.sequential.Greens)
fig5 = fig5.update_layout(xaxis_title="Popularity", yaxis_title="Electric Vehicle Models", showlegend=False)

# Top 3 manufacturer and top models among them
top_manu = df["Make"].value_counts()[:3]
top_manuf_data = df[df["Make"].isin(top_manu.index)]
top_models = top_manuf_data.groupby(["Make","Model"]).size().sort_values(ascending = False).reset_index(name = "Number of vehicles")[:10]
fig6 = px.bar(x = top_models["Model"], y = top_models["Number of vehicles"],color = top_models["Make"], title = "VI : Top 3 manufacturer and top models among them")

# Electric range of vehicles
fig7 = px.histogram(x = df["Electric Range"], nbins = 30, title = "VII : Electric range of vehicles")

# Calculating the average electric range by model year
avg_by_year = df.groupby("Model Year")["Electric Range"].mean().reset_index()
fig8 = px.line(x = avg_by_year["Model Year"], y = avg_by_year["Electric Range"], title = "VIII : Average Electric Range by Model Year")
fig8 = fig8.update_layout(xaxis_title="Model Year", yaxis_title="Electric Range")

# Let’s explore how electric ranges vary among the top manufacturers and models
da = top_manuf_data.groupby(["Model","Make"])["Electric Range"].mean().sort_values(ascending = False).reset_index(name = "Avg Range")[:10]
fig9 = px.bar(x = da["Avg Range"], y = da["Model"], color = da["Make"], title = "IX : Top 10 Models by Average Electric Range in Top Makes")

# Calculate the number of EVs registered each year
regis_each_year = df["Model Year"].value_counts()
fig10 = px.bar(x = regis_each_year.index, y = regis_each_year.values, title = "X : The number of EVs registered each year")



app.layout = html.Div(
    children = [
        html.H1(children = 'Electric Vehicle Analytics'),
        html.P(
            children = "Analyze the behavior of electric vehicle adoption and electric range over model years."
        ),
        dcc.Graph(
            figure = fig1
        ),
        dcc.Graph(
            figure = fig2
        ),
        dcc.Graph(
            figure = fig3
        ),
        dcc.Graph(
            figure = fig4
        ),
        dcc.Graph(
            figure = fig5
        ),
        dcc.Graph(
            figure = fig6
        ),
        dcc.Graph(
            figure = fig7
        ),
        dcc.Graph(
            figure = fig8
        ),
        dcc.Graph(
            figure = fig9
        ),
        dcc.Graph(
            figure = fig10
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)