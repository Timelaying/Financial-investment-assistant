import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Portfolio Goals",
    page_icon="💼"
)

# Main header
st.title("Portfolio Goals")

# Introduction
st.write(
    """
    Welcome to the Portfolio Goals page! Here, you can define your investment objectives and preferences.
    Please fill out the following fields to help us tailor investment recommendations for you.
    """
)

# Form for users to fill their portfolio goals
with st.expander("Fill Your Portfolio Goals"):
    goal1 = st.text_input("Goal 1", "")
    goal2 = st.text_input("Goal 2", "")
    goal3 = st.text_input("Goal 3", "")

# Risk tolerance
st.subheader("Risk Tolerance")
risk_tolerance = st.selectbox(
    "Select your risk tolerance",
    ["Low - I prefer stability over potential returns",
     "Medium - I'm comfortable with moderate fluctuations",
     "High - I'm willing to take high risks for potential high returns"]
)

# Investment horizon
st.subheader("Investment Horizon")
investment_horizon = st.selectbox(
    "Select your investment horizon",
    ["Short-term - 1 to 3 years",
     "Medium-term - 3 to 5 years",
     "Long-term - 5 years or more"]
)

# Investment amount
st.subheader("Investment Amount")
investment_amount = st.number_input(
    "Enter your investment amount ($)",
    min_value=0.0,
    step=100.0,
    value=1000.0
)

# Types of stocks 
st.subheader("Types of Stocks")
types_of_stocks = st.multiselect(
    "Select types of stocks you're interested in",
    ["Technology", "Finance", "Healthcare", "Consumer Goods"]
)

# Investment style
st.subheader("Investment Style")
investment_style = st.radio(
    "Select your investment style",
    ["Value Investing", "Growth Investing", "Index Investing"]
)

# Button to submit portfolio goals
if st.button("Submit"):
    # Display confirmation message
    st.success("Portfolio goals submitted successfully!")
