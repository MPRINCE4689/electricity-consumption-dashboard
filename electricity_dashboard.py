import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import io

# Configure page
st.set_page_config(
    page_title="Electricity Consumption Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("⚡ Electricity Consumption Dashboard")
st.markdown("Track electricity usage and costs per household or department")

# Sidebar for data input options
st.sidebar.header("Data Input Options")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Upload CSV File", "Manual Data Entry", "Use Sample Data"]
)

# Function to create sample data
def create_sample_data():
    """Create sample electricity consumption data"""
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    units = ["Kitchen", "Living Room", "Bedroom", "Office", "Garage"]
    
    data = []
    for month in months:
        for unit in units:
            # Generate realistic consumption and cost data
            base_consumption = np.random.normal(100, 20)  # kWh
            cost_per_unit = np.random.uniform(0.10, 0.15)  # $/kWh
            consumption = max(50, base_consumption)  # Minimum 50 kWh
            cost = consumption * cost_per_unit
            
            data.append({
                "Month": month,
                "UnitName": unit,
                "UnitsConsumed": round(consumption, 2),
                "Cost": round(cost, 2)
            })
    
    return pd.DataFrame(data)

# Data loading based on user selection
if input_method == "Upload CSV File":
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file", 
        type="csv",
        help="Upload a CSV file with columns: Month, UnitName, UnitsConsumed, Cost"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("File uploaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
            df = create_sample_data()
    else:
        st.sidebar.info("Please upload a CSV file or use sample data")
        df = create_sample_data()

elif input_method == "Manual Data Entry":
    st.sidebar.subheader("Enter Data Manually")
    
    # Create form for manual data entry
    with st.sidebar.form("manual_entry"):
        month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", 
                                     "July", "August", "September", "October", "November", "December"])
        unit_name = st.text_input("Unit Name", placeholder="e.g., Kitchen")
        units_consumed = st.number_input("Units Consumed (kWh)", min_value=0.0, step=0.1)
        cost = st.number_input("Cost ($)", min_value=0.0, step=0.01)
        
        submitted = st.form_submit_button("Add Entry")
        
        if submitted and unit_name:
            # Initialize session state for manual data
            if 'manual_data' not in st.session_state:
                st.session_state.manual_data = []
            
            st.session_state.manual_data.append({
                "Month": month,
                "UnitName": unit_name,
                "UnitsConsumed": units_consumed,
                "Cost": cost
            })
            st.sidebar.success("Entry added!")
    
    # Use manual data if available, otherwise sample data
    if 'manual_data' in st.session_state and st.session_state.manual_data:
        df = pd.DataFrame(st.session_state.manual_data)
    else:
        df = create_sample_data()
        
else:  # Use Sample Data
    df = create_sample_data()
    st.sidebar.info("Using sample data for demonstration")

# Display data preview
st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)

# Data validation
required_columns = ["Month", "UnitName", "UnitsConsumed", "Cost"]
if not all(col in df.columns for col in required_columns):
    st.error(f"CSV file must contain columns: {', '.join(required_columns)}")
    st.stop()

# Calculate KPIs
total_units = df['UnitsConsumed'].sum()
total_cost = df['Cost'].sum()
avg_cost_per_unit = total_cost / total_units if total_units > 0 else 0
num_departments = df['UnitName'].nunique()

# Display KPIs
st.subheader("📊 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Units Consumed",
        value=f"{total_units:,.2f} kWh",
        delta=None
    )

with col2:
    st.metric(
        label="Total Cost",
        value=f"${total_cost:,.2f}",
        delta=None
    )

with col3:
    st.metric(
        label="Average Cost per kWh",
        value=f"${avg_cost_per_unit:.3f}",
        delta=None
    )

with col4:
    st.metric(
        label="Number of Units/Departments",
        value=f"{num_departments}",
        delta=None
    )

# Create visualizations
st.subheader("📈 Visualizations")

# 1. Monthly consumption trend (Line Chart)
st.subheader("Monthly Consumption Trend")
monthly_data = df.groupby('Month')['UnitsConsumed'].sum().reset_index()

# Order months correctly
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
monthly_data['Month'] = pd.Categorical(monthly_data['Month'], categories=month_order, ordered=True)
monthly_data = monthly_data.sort_values('Month')

fig_line = px.line(
    monthly_data, 
    x='Month', 
    y='UnitsConsumed',
    title='Monthly Electricity Consumption Trend',
    labels={'UnitsConsumed': 'Units Consumed (kWh)', 'Month': 'Month'},
    markers=True
)
fig_line.update_layout(
    xaxis_title="Month",
    yaxis_title="Units Consumed (kWh)",
    hovermode='x unified'
)
st.plotly_chart(fig_line, use_container_width=True)

# 2. Usage by department/unit (Bar Chart)
st.subheader("Usage by Department/Unit")
unit_data = df.groupby('UnitName')['UnitsConsumed'].sum().reset_index().sort_values('UnitsConsumed', ascending=True)

fig_bar = px.bar(
    unit_data,
    x='UnitsConsumed',
    y='UnitName',
    orientation='h',
    title='Electricity Consumption by Department/Unit',
    labels={'UnitsConsumed': 'Units Consumed (kWh)', 'UnitName': 'Department/Unit'},
    color='UnitsConsumed',
    color_continuous_scale='Blues'
)
fig_bar.update_layout(
    xaxis_title="Units Consumed (kWh)",
    yaxis_title="Department/Unit"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 3. Cost Analysis
st.subheader("Cost Analysis")
col1, col2 = st.columns(2)

with col1:
    # Monthly cost trend
    monthly_cost = df.groupby('Month')['Cost'].sum().reset_index()
    monthly_cost['Month'] = pd.Categorical(monthly_cost['Month'], categories=month_order, ordered=True)
    monthly_cost = monthly_cost.sort_values('Month')
    
    fig_cost = px.line(
        monthly_cost,
        x='Month',
        y='Cost',
        title='Monthly Cost Trend',
        labels={'Cost': 'Cost ($)', 'Month': 'Month'},
        markers=True
    )
    fig_cost.update_traces(line_color='red')
    st.plotly_chart(fig_cost, use_container_width=True)

with col2:
    # Cost by department (Pie Chart)
    unit_cost = df.groupby('UnitName')['Cost'].sum().reset_index()
    
    fig_pie = px.pie(
        unit_cost,
        values='Cost',
        names='UnitName',
        title='Cost Distribution by Department/Unit'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 4. Detailed Analysis Table
st.subheader("Detailed Analysis")
analysis_option = st.selectbox(
    "Select Analysis View:",
    ["Monthly Summary", "Department Summary", "Detailed Records"]
)

if analysis_option == "Monthly Summary":
    monthly_summary = df.groupby('Month').agg({
        'UnitsConsumed': ['sum', 'mean'],
        'Cost': ['sum', 'mean']
    }).round(2)
    monthly_summary.columns = ['Total Units', 'Avg Units', 'Total Cost', 'Avg Cost']
    st.dataframe(monthly_summary, use_container_width=True)

elif analysis_option == "Department Summary":
    dept_summary = df.groupby('UnitName').agg({
        'UnitsConsumed': ['sum', 'mean', 'max', 'min'],
        'Cost': ['sum', 'mean', 'max', 'min']
    }).round(2)
    dept_summary.columns = ['Total Units', 'Avg Units', 'Max Units', 'Min Units', 
                           'Total Cost', 'Avg Cost', 'Max Cost', 'Min Cost']
    st.dataframe(dept_summary, use_container_width=True)

else:
    st.dataframe(df, use_container_width=True)

# Export functionality
st.subheader("📥 Export Data")
col1, col2 = st.columns(2)

with col1:
    # Export current data as CSV
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv_data,
        file_name=f"electricity_consumption_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col2:
    # Export summary report
    if st.button("Generate Summary Report"):
        report = f"""
        ELECTRICITY CONSUMPTION SUMMARY REPORT
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        KEY METRICS:
        - Total Units Consumed: {total_units:,.2f} kWh
        - Total Cost: ${total_cost:,.2f}
        - Average Cost per kWh: ${avg_cost_per_unit:.3f}
        - Number of Departments/Units: {num_departments}
        
        TOP CONSUMING DEPARTMENTS:
        {unit_data.nlargest(3, 'UnitsConsumed')[['UnitName', 'UnitsConsumed']].to_string(index=False)}
        
        MONTHLY TRENDS:
        Highest consumption month: {monthly_data.loc[monthly_data['UnitsConsumed'].idxmax(), 'Month']}
        Lowest consumption month: {monthly_data.loc[monthly_data['UnitsConsumed'].idxmin(), 'Month']}
        """
        
        st.download_button(
            label="Download Summary Report",
            data=report,
            file_name=f"electricity_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("**Dashboard created with Streamlit for Electricity Consumption Analysis**")
