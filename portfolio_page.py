import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Portfolio Goals",
    page_icon="💼"
)

# Main header
st.title("Portfolio Goals")

# Form for users to fill their portfolio goals
st.subheader("Fill Your Portfolio Goals")

# Input fields for portfolio goals
goal1 = st.text_input("Goal 1", "")
goal2 = st.text_input("Goal 2", "")
goal3 = st.text_input("Goal 3", "")

# Button to submit portfolio goals
if st.button("Submit"):
    # Display confirmation message
    st.success("Portfolio goals submitted successfully!")
