import streamlit as st
import pandas as pd
from core.scenario import Scenario
from core.accounts import SavingsAccount

st.title("LISA Calculator")

# Initialize a counter for the number of account UIs if not already done
if "accounts_ui" not in st.session_state:
    st.session_state.accounts_ui = 1

# Button to add an account UI in the same row
def add_account():
    st.session_state.accounts_ui += 1

st.button("Add Account", on_click=add_account)

# Create containers (columns) for each account UI
cols = st.columns(st.session_state.accounts_ui)
account_inputs = []

# Loop through each account container to collect inputs
for i, col in enumerate(cols):
    with col:
        st.markdown(f"### Account {i+1}")
        # Choose account type
        account_type = st.segmented_control(
            "Account Type", ["ISA", "LISA"],
            selection_mode="single", key=f"account_type_{i}", default="ISA"
        )
        max_deposit = {"ISA": 20000, "LISA": 4000}
        deposit = st.number_input(
            "Deposit Amount",
            min_value=0,
            max_value=max_deposit[account_type],
            value=0,
            step=100,
            key=f"deposit_amount_{i}"
        )
        interest_rate = st.number_input(
            "Interest Rate (AER%)",
            min_value=0.0,
            max_value=50.0,
            value=5.0,
            step=0.1,
            key=f"interest_rate_{i}"
        )
        account_inputs.append({
            "type": account_type.lower(),
            "deposit": deposit,
            "interest_rate": interest_rate
        })

# Common scenario inputs outside of account definitions
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

# Create scenario and add each account with its own parameters
scenario = Scenario()
for idx, account_def in enumerate(account_inputs):
    account = SavingsAccount(account_def["type"])
    scenario.add_account(account, {"interest_rate": account_def["interest_rate"],
                                   "deposit": account_def["deposit"]})

# Run the simulation (year-by-year history is recorded internally)
scenario.run(years)

# Build a DataFrame for the line chart using get_history (list of lists)
# Convert the list of account histories into a dict with keys "Account 1", "Account 2", etc.
history_raw = scenario.get_history()  # returns List[List[float]]
history_dict = {f"Account {i+1}": history for i, history in enumerate(history_raw)}
df_history = pd.DataFrame(history_dict, index=range(1, years + 1))
st.line_chart(df_history)

# Withdraw for the house purchase and display the final savings as a big metric
saved_total = scenario.withdraw(house_price * 1000)
st.metric(label="Total Savings After Withdrawal", value=f"£{saved_total:,.2f}")

# Display the remaining savings per account underneath
st.markdown("### Savings by Account After Withdrawal")
for idx, account in enumerate(scenario.get_accounts()):
    st.write(f"**Account {idx+1}:** £{account.balance:,.2f}")