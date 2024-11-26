# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from io import BytesIO

# # Initialize session state to store expenses
# if "expenses" not in st.session_state:
#     st.session_state.expenses = []

# # Title
# st.title("💰 Personal Expense Tracker")
# st.write("Track and visualize your personal expenses easily!")

# # Input for adding a new expense
# st.header("Add a New Expense")
# col1, col2, col3 = st.columns(3)

# with col1:
#     amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
# with col2:
#     category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Other"])
# with col3:
#     description = st.text_input("Description")

# # Button to add expense
# if st.button("Add Expense"):
#     if amount > 0:
#         st.session_state.expenses.append({"Amount": amount, "Category": category, "Description": description})
#         st.success("Expense added!")
#     else:
#         st.error("Amount must be greater than 0.")

# # Display the expense table
# if st.session_state.expenses:
#     st.header("Expense History")
#     df = pd.DataFrame(st.session_state.expenses)
#     st.dataframe(df)

#     # Summary of expenses by category
#     st.header("Spending Summary")
#     summary = df.groupby("Category")["Amount"].sum().reset_index()
#     st.write(summary)

#     # Visualize spending
#     st.header("Spending Visualization")
#     fig, ax = plt.subplots()
#     ax.pie(summary["Amount"], labels=summary["Category"], autopct="%1.1f%%", startangle=90)
#     ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
#     st.pyplot(fig)

#     # Download expenses as CSV
#     st.header("Download Data")
#     csv = df.to_csv(index=False)
#     st.download_button(
#         label="Download CSV",
#         data=csv,
#         file_name="expenses.csv",
#         mime="text/csv",
#     )
# else:
#     st.write("No expenses recorded yet. Add your first expense!")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from io import BytesIO

# Initialize session state to store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Page Configuration
st.set_page_config(
    page_title="💰 Personal Expense Tracker",
    page_icon="💵",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-menu {font-family: Arial, sans-serif; color: white; font-size: 20px;}
    .add-expense-btn {background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer;}
    .add-expense-btn:hover {background-color: #45a049;}
    .download-btn {background-color: #007BFF; color: white; padding: 10px 20px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer;}
    .download-btn:hover {background-color: #0056b3;}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Add Expense", "View History", "Analytics"],
        icons=["plus-circle", "table", "bar-chart"],
        menu_icon="cast",
        default_index=0,
    )

# Add Expense Section
if selected == "Add Expense":
    st.title("💳 Add Your Expense")
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Other"])
    with col3:
        description = st.text_input("Description")

    if st.button("Add Expense", key="add_btn", help="Click to add your expense"):
        if amount > 0:
            st.session_state.expenses.append({"Amount": amount, "Category": category, "Description": description})
            st.success("Expense added successfully!")
        else:
            st.error("Amount must be greater than 0.")

# View History Section
if selected == "View History":
    st.title("📜 Expense History")
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        category_filter = st.selectbox("Filter by Category", ["All"] + df["Category"].unique().tolist())
        filtered_df = df if category_filter == "All" else df[df["Category"] == category_filter]
        st.dataframe(filtered_df)

        # Download Button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="expenses.csv",
            mime="text/csv",
            key="download_csv",
        )
    else:
        st.write("No expenses recorded yet.")

# Analytics Section
if selected == "Analytics":
    st.title("📊 Expense Analytics")
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)

        # Spending Summary
        st.subheader("Spending Summary by Category")
        summary = df.groupby("Category")["Amount"].sum().reset_index()
        st.write(summary)

        # Visualization
        st.subheader("Spending Visualization")

        # Pie Chart
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Pie Chart**")
            fig1, ax1 = plt.subplots()
            ax1.pie(summary["Amount"], labels=summary["Category"], autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
            ax1.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
            st.pyplot(fig1)

        # Bar Chart
        with col2:
            st.write("**Bar Chart**")
            fig2, ax2 = plt.subplots()
            ax2.bar(summary["Category"], summary["Amount"], color=plt.cm.Paired.colors[:len(summary["Category"])])
            ax2.set_ylabel("Amount")
            ax2.set_title("Spending by Category")
            st.pyplot(fig2)

    else:
        st.write("No expenses recorded yet. Add some data to view analytics.")
