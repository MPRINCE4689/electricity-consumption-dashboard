# ⚡ Electricity Consumption Dashboard

A Python web dashboard for tracking electricity usage and costs using Streamlit, Pandas, and Plotly.

## Features
- 📊 Interactive KPIs (Total units, costs, averages)
- 📈 Monthly consumption trends (Line charts)
- 📊 Department usage comparison (Bar charts)
- 💰 Cost analysis and distribution
- 📥 CSV upload, manual entry, or sample data
- 📤 Export data and reports

## Quick Start

### 1. Install Python 3.7+
Download from [python.org](https://python.org/downloads/) (✅ Check "Add to PATH")

### 2. Setup Project
```bash
# Create project folder
mkdir electricity-dashboard
cd electricity-dashboard

# Create virtual environment
python -m venv dashboard_env
dashboard_env\Scripts\activate  # Windows
# source dashboard_env/bin/activate  # Mac/Linux

# Install packages
pip install streamlit pandas plotly numpy openpyxl
```

### 3. Create Files
Create `electricity_dashboard.py` with the provided code and `sample_data.csv` with sample data.

### 4. Run Dashboard
```bash
streamlit run electricity_dashboard.py
```
Opens automatically at `http://localhost:8501`

## Data Format
CSV file with columns: `Month`, `UnitName`, `UnitsConsumed`, `Cost`

```csv
Month,UnitName,UnitsConsumed,Cost
January,Kitchen,120.5,18.08
January,Office,95.2,14.28
```

## Usage
1. Select data input method (Upload CSV / Manual Entry / Sample Data)
2. View KPIs and interactive charts
3. Analyze monthly trends and department usage
4. Export data and reports

## Troubleshooting
- **Module not found**: Activate virtual environment and reinstall packages
- **Streamlit not found**: Use `python -m streamlit run electricity_dashboard.py`
- **Port in use**: Add `--server.port 8502` to command

## Project Structure

electricity-dashboard/
├── dashboard_env/              # Virtual environment
├── electricity_dashboard.py    # Main application
├── requirements.txt            # Package dependencies
├── sample_data.csv            # Sample data file
├── test_setup.py              # Setup verification script
├── quick_start.bat            # Windows quick start script
└── README.md                  # Project documentation



**Made with Python + Streamlit for electricity consumption analysis**
