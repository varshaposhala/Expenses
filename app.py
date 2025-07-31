import streamlit as st
import pandas as pd
import os
import json

# File paths
EXPENSES_FILE = "expenses.json"
BALANCE_FILE = "balance.txt"

# Load data
def load_data():
    expenses = []
    balance = 0.0

    # Load expenses
    if os.path.exists(EXPENSES_FILE):
        try:
            with open(EXPENSES_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    expenses = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            expenses = []  # Reset corrupted file
            st.warning("⚠️ 'expenses.json' was corrupted or empty. Starting fresh.")

    # Load balance
    if os.path.exists(BALANCE_FILE):
        try:
            with open(BALANCE_FILE, "r") as f:
                balance_str = f.read().strip()
                if balance_str:
                    balance = float(balance_str)
        except ValueError:
            balance = 0.0
            st.warning("⚠️ 'balance.txt' was corrupted or empty. Resetting balance.")

    return expenses, balance

# Save data
def save_data(expenses, balance):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f)
    with open(BALANCE_FILE, "w") as f:
        f.write(str(balance))

# Load initial data into session state
if "expenses" not in st.session_state or "balance" not in st.session_state:
    expenses, balance = load_data()
    st.session_state.expenses = expenses
    st.session_state.balance = balance

st.title("💸 Persistent Expense Manager")

# Add to Balance
st.subheader("Add Money to Your Balance")
initial_input = st.number_input("Enter amount", min_value=0.0, step=1.0, format="%.2f")
if st.button("Add to Balance"):
    st.session_state.balance += initial_input
    save_data(st.session_state.expenses, st.session_state.balance)
    st.success(f"Added ₹{initial_input:.2f} to your balance")

# Add Expense
st.subheader("Log an Expense")
reason = st.text_input("Reason")
category = st.selectbox("Category", ["Food", "Transport", "Bills", "Fun", "Health", "Other"])
amount = st.number_input("Amount", min_value=0.0, step=1.0, format="%.2f")

if st.button("Add Expense"):
    if amount <= st.session_state.balance:
        expense = {"Reason": reason, "Category": category, "Amount": amount}
        st.session_state.expenses.append(expense)
        st.session_state.balance -= amount
        save_data(st.session_state.expenses, st.session_state.balance)
        st.success(f"Added expense: {reason} - ₹{amount:.2f}")
    else:
        st.error("Not enough balance!")

# Show Balance and Table
st.subheader("💰 Current Balance")
st.info(f"₹{st.session_state.balance:.2f}")

if st.session_state.expenses:
    st.subheader("📒 Expenses")
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df, use_container_width=True)
