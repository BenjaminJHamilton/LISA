import streamlit as st
import pandas as pd
from core.scenario import Scenario
from core.accounts import SavingsAccount

st.title("LISA Calculator")

# Function to create account inputs for a scenario
def create_account_inputs(scenario_name, column, max_accounts=2):
    column.markdown(f"## {scenario_name}")
    account_inputs = []
    for i in range(max_accounts):
        column.markdown(f"### Account {i+1}")
        account_type = column.selectbox(
            "Account Type",
            ["ISA", "LISA"],
            key=f"{scenario_name}_account_type_{i}"
        )
        max_deposit = {"ISA": 20000, "LISA": 4000}
        deposit = column.number_input(
            "Yearly Deposit Amount",
            min_value=0,
            max_value=max_deposit[account_type],
            value=0,
            step=100,
            key=f"{scenario_name}_deposit_amount_{i}"
        )
        interest_rate = column.number_input(
            "Interest Rate (AER%)",
            min_value=0.0,
            max_value=50.0,
            value=5.0,
            step=0.1,
            key=f"{scenario_name}_interest_rate_{i}"
        )
        account_inputs.append({
            "type": account_type.lower(),
            "deposit": deposit,
            "interest_rate": interest_rate
        })
    return account_inputs

# Create two columns for side-by-side scenario inputs
col1, col2 = st.columns(2)

# Collect inputs for Scenario 1 and Scenario 2
scenario_1_inputs = create_account_inputs("Scenario 1", column=col1)
scenario_2_inputs = create_account_inputs("Scenario 2", column=col2)

# Common inputs for both scenarios
st.markdown("## Common Inputs")
years = st.number_input(
    "Number of Years",
    min_value=1,
    max_value=50,
    value=5,
    step=1,
    key="years"
)

house_price = st.number_input(
    "House Price (£thousands)",
    min_value=0,
    max_value=10000,
    value=350,
    step=10,
    key="house_price"
)

# Function to create and run a scenario
def create_and_run_scenario(account_inputs, years):
    scenario = Scenario()
    for account_def in account_inputs:
        account = SavingsAccount(account_def["type"])
        scenario.add_account(account, {"interest_rate": account_def["interest_rate"],
                                       "deposit": account_def["deposit"]})
    scenario.run(years)
    return scenario

# Create and run both scenarios
scenario_1 = create_and_run_scenario(scenario_1_inputs, years)
scenario_2 = create_and_run_scenario(scenario_2_inputs, years)

# Display results for both scenarios
st.markdown("## Results Comparison")

# Display total savings after withdrawal for both scenarios
saved_total_1 = scenario_1.withdraw(house_price * 1000)
saved_total_2 = scenario_2.withdraw(house_price * 1000)

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Savings After Withdrawal (Scenario 1)", value=f"£{saved_total_1:,.2f}")
with col2:
    st.metric(label="Total Savings After Withdrawal (Scenario 2)", value=f"£{saved_total_2:,.2f}")


# Build DataFrames for line charts
history_1 = scenario_1.get_history()
history_2 = scenario_2.get_history()

history_dict_1 = {f"Scenario 1 - Account {i+1}": history for i, history in enumerate(history_1)}
history_dict_2 = {f"Scenario 2 - Account {i+1}": history for i, history in enumerate(history_2)}

df_history_1 = pd.DataFrame(history_dict_1, index=range(1, years + 1))
df_history_2 = pd.DataFrame(history_dict_2, index=range(1, years + 1))

# Display line charts side by side
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Scenario 1")
    st.line_chart(df_history_1)
with col2:
    st.markdown("### Scenario 2")
    st.line_chart(df_history_2)

