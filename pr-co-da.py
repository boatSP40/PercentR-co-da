import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Set the page configuration
st.set_page_config(page_title="Automate Percent Reflection Data Stacking",
                   page_icon="📈",
                   layout="wide")

# Machine selection
machine_options = ["RU-III", "BCSP"]
selected_machine = st.selectbox("Select Machine", machine_options)

# File upload
if selected_machine in ["RU-III"]:
    uploaded_file = st.file_uploader("Upload an Excel File", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(
            io=uploaded_file,
            engine='openpyxl',
            sheet_name=None,
            usecols='A:AZ',
            nrows=1000000
        )

        # Sheet selection
        sheet_name = st.selectbox("Select Sheet", list(df.keys()))
        df = df[sheet_name]

        # Sidebar selections
        coat_date = st.sidebar.multiselect("Select the Coated Date:", options=df["Coat_Date"].unique(), default=df["Coat_Date"].unique())
        coat_side = st.sidebar.multiselect("Select the Coat Side:", options=df["Coat_Side"].unique(), default=df["Coat_Side"].unique())

        # Filter the dataframe based on selections
        df_selection = df.query("Coat_Date == @coat_date & Coat_Side == @coat_side")
        df_selection["Coat_Date"] = df_selection["Coat_Date"].dt.date

        # Line Chart with Plotly
        st.subheader("Percent R Stacking📈")
        grouped_df = df_selection.groupby("Coat_Date")
        top_line_plotly = go.Figure()

        # Define the number of data points per set
        data_points_per_set = 401

        for coat_date, group in grouped_df:
            # Split the data into sets of 401 data points
            sets = np.arange(len(group)) // data_points_per_set

            for set_id, set_group in group.groupby(sets):
                x_values = set_group["wave"].values

                for column in ['T', 'M', 'L1', 'L2', 'Spec']:
                    top_line_plotly.add_trace(go.Scatter(x=x_values, y=set_group[column],
                                                         mode="lines",
                                                         name=f"Coat_Date: {coat_date} - {column} - Start Time: {set_group['Start_Time'].iloc[0]}",
                                                         textposition="top center"))

        # Update layout
        top_line_plotly.update_layout(title="Top Layer",
                                      yaxis_title="Percent Reflection",
                                      width=1000, height=600,
                                      showlegend=True)

        # Color change buttons
        color_by_date = st.button("Change Color by Coat_Date")
        color_by_column = st.button("Change Color by Column")

        css = """
        <style>
        """

        # Recreate the chart based on the selected color option
        if color_by_date:
            date_colors = dict(zip(df_selection["Coat_Date"].unique(), px.colors.qualitative.Plotly))
            for i, trace in enumerate(top_line_plotly.data):
                try:
                    coat_date = trace.name.split(" - ")[1].split(" - ")[0]
                    color = date_colors[coat_date]
                    trace.marker.color = color
                    css += f".svg-container .plotly .scatterlayer .trace-{i + 1} {{ stroke: {color} !important; fill: {color} !important; }}\n"
                except KeyError:
                    pass

        if color_by_column:
            for i, trace in enumerate(top_line_plotly.data):
                try:
                    column_name = trace.name.split(" - ")[3].split(" - ")[0]
                    color = px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                    trace.marker.color = color
                    css += f".svg-container .plotly .scatterlayer .trace-{i + 1} {{ stroke: {color} !important; fill: {color} !important; }}\n"
                except IndexError:
                    pass

        css += """
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

        # Display the plot
        st.plotly_chart(top_line_plotly)
    else:
        st.warning("Please upload a file.")


if selected_machine in ["BCSP"]:
    uploaded_file = st.file_uploader("Upload an Excel File", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(
            io=uploaded_file,
            engine='openpyxl',
            sheet_name=None,
            usecols='A:AZ',
            nrows=1000000
        )

        # Sheet selection
        sheet_name = st.selectbox("Select Sheet", list(df.keys()))
        df = df[sheet_name]

        # Sidebar selections
        coat_date = st.sidebar.multiselect("Select the Coated Date:", options=df["Coat_Date"].unique(), default=df["Coat_Date"].unique())
        coat_side = st.sidebar.multiselect("Select the Coat Side:", options=df["Coat_Side"].unique(), default=df["Coat_Side"].unique())

        # Filter the dataframe based on selections
        df_selection = df.query("Coat_Date == @coat_date & Coat_Side == @coat_side")
        df_selection["Coat_Date"] = df_selection["Coat_Date"].dt.date

        # Line Chart with Plotly
        st.subheader("Percent R Stacking📈")
        grouped_df = df_selection.groupby("Coat_Date")
        top_line_plotly = go.Figure()

        # Define the number of data points per set
        data_points_per_set = 602

        for coat_date, group in grouped_df:
            # Split the data into sets of 599 data points
            sets = np.arange(len(group)) // data_points_per_set

            for set_id, set_group in group.groupby(sets):
                x_values = set_group["wave"].values

                for column in ['T', 'M', 'L1', 'L2']:
                    top_line_plotly.add_trace(go.Scatter(x=x_values, y=set_group[column],
                                                         mode="lines",
                                                         name=f"Coat_Date: {coat_date} - {column} - Start Time: {set_group['Start_Time'].iloc[0]}",
                                                         textposition="top center"))

        # Update layout
        top_line_plotly.update_layout(title="Top Layer",
                                      yaxis_title="Percent Reflection",
                                      width=1000, height=600,
                                      showlegend=True)

        # Color change buttons
        color_by_date = st.button("Change Color by Coat_Date")
        color_by_column = st.button("Change Color by Column")

        css = """
        <style>
        """

        # Recreate the chart based on the selected color option
        if color_by_date:
            date_colors = dict(zip(df_selection["Coat_Date"].unique(), px.colors.qualitative.Plotly))
            for i, trace in enumerate(top_line_plotly.data):
                try:
                    coat_date = trace.name.split(" - ")[1].split(" - ")[0]
                    color = date_colors[coat_date]
                    trace.marker.color = color
                    css += f".svg-container .plotly .scatterlayer .trace-{i + 1} {{ stroke: {color} !important; fill: {color} !important; }}\n"
                except KeyError:
                    pass

        if color_by_column:
            for i, trace in enumerate(top_line_plotly.data):
                try:
                    column_name = trace.name.split(" - ")[3].split(" - ")[0]
                    color = px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                    trace.marker.color = color
                    css += f".svg-container .plotly .scatterlayer .trace-{i + 1} {{ stroke: {color} !important; fill: {color} !important; }}\n"
                except IndexError:
                    pass

        css += """
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

        # Display the plot
        st.plotly_chart(top_line_plotly)
    else:
        st.warning("Please upload a file.")
