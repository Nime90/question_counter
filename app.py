from datetime import datetime
import gspread
import pandas as pd
import streamlit as st

# Setup Page
st.set_page_config(page_title="Group Question Tracker", layout="centered")

# Sheet Details
SPREADSHEET_ID = "11SsaBKKAMCVjpujPKQYmtIukGOisA0uLFMImq3CoRs4"


# Authenticate with Google Sheets using gspread
@st.cache_resource
def get_gsheet_client():
    return gspread.service_account(filename="service_account.json")


# Connect to worksheet
try:
    gc = get_gsheet_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.sheet1
except Exception as e:
    st.error(f"Failed to connect to Google Sheets: {e}")
    st.stop()


# Helper function to read current sheet data
def load_data():
    records = worksheet.get_all_records()
    return pd.DataFrame(records)


# Navigation Tabs
tab1, tab2 = st.tabs(["📝 Ask a Question", "🏆 Group Rankings & Analytics"])

# =============================================================================
# TAB 1: Submit Question
# =============================================================================
with tab1:
    st.header("Submit Your Question")

    with st.form(key="question_form"):
        selected_group = st.selectbox(
            label="Select your group:",
            options=[f"Group {i}" for i in range(1, 8)],
        )

        user_question = st.text_area(
            label="Type your question here:",
            placeholder="What would you like to ask?",
        )

        submit_button = st.form_submit_button(label="Submit Question")

    if submit_button:
        if user_question.strip() == "":
            st.warning("Please type a question before submitting.")
        else:
            try:
                # Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Append row directly to the sheet: [Group, Question, Timestamp]
                worksheet.append_row([selected_group, user_question, timestamp])

                st.success("Your question has been submitted successfully!")

            except Exception as e:
                st.error(f"Error submitting question: {e}")


# =============================================================================
# TAB 2: Group Rankings & Time Series Analysis
# =============================================================================
with tab2:
    st.header("Analytics & Rankings")

    try:
        df = load_data()

        if (
            df.empty
            or "Group" not in df.columns
            or "Timestamp" not in df.columns
        ):
            st.info("No questions have been submitted yet.")
        else:
            # --- SECTION 1: Total Question Count Table ---
            st.subheader("🏆 Total Questions per Group")
            ranking = df["Group"].value_counts().reset_index()
            ranking.columns = ["Group Name", "Total Questions Asked"]
            st.dataframe(ranking, use_container_width=True, hide_index=True)

            st.divider()

            # --- SECTION 2: Time Series Analysis ---
            st.subheader("📈 Questions Over Time")

            # Convert Timestamp column to datetime format
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])

            # Sort data chronologically
            df = df.sort_values("Timestamp")

            # Count each submission as 1 question
            df["Question_Count"] = 1

            # Pivot data: Rows = Timestamps, Columns = Groups
            time_df = df.pivot_table(
                index="Timestamp",
                columns="Group",
                values="Question_Count",
                aggfunc="sum",
            ).fillna(0)

            # Ensure all Groups (1 through 7) exist as columns even if they haven't asked questions yet
            all_groups = [f"Group {i}" for i in range(1, 8)]
            for group in all_groups:
                if group not in time_df.columns:
                    time_df[group] = 0.0

            # Calculate running cumulative total for each group over time
            cumulative_df = time_df[all_groups].cumsum()

            # Display line chart
            st.line_chart(cumulative_df)

    except Exception as e:
        st.error(f"Could not fetch analytics: {e}")