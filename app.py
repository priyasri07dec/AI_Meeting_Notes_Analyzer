import streamlit as st
import pandas as pd

from graph import meeting_graph

# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    page_icon="📝",
    layout="wide"
)

# HEADER

st.title("📝 AI Meeting Notes Analyzer")

st.markdown(
    """
    **AI-powered meeting analysis using Gemini and LangGraph**

    Extract key topics, generate meeting summaries, identify action
    items, deadlines, owners, and classify task priorities from a
    meeting transcript.
    """
)

st.divider()

# INPUT SECTION

st.subheader("📄 Meeting Transcript")

transcript = st.text_area(
    "Paste your meeting transcript below:",
    height=300,
    placeholder=(
        "Example:\n\n"
        "John: We need to improve the website performance.\n"
        "David: I will optimize the database queries this week.\n"
        "Sarah: I will redesign the homepage layout.\n"
        "John: Let's finish these tasks before Friday."
    )
)

# ANALYZE BUTTON

analyze_button = st.button(
    "🔍 Analyze Meeting",
    type="primary",
    use_container_width=True
)


if analyze_button:

    # INPUT VALIDATION

    if not transcript.strip():

        st.warning(
            "Please enter a meeting transcript before analyzing."
        )

    else:

        with st.spinner("Analyzing meeting transcript..."):

            initial_state = {
                "transcript": transcript,
                "topics": [],
                "summary": "",
                "action_items": [],
                "priority": [],
                "final_report": ""
            }

            try:

                # RUN LANGGRAPH WORKFLOW

                result = meeting_graph.invoke(initial_state)

                st.success(
                    "Meeting analysis completed successfully!"
                )

                st.divider()

                # KEY TOPICS

                st.subheader("🔑 Key Topics")

                topics = result.get("topics", [])

                if topics:

                    for topic in topics:
                        st.markdown(f"- {topic}")

                else:

                    st.info("No key topics were identified.")


                st.divider()

                # MEETING SUMMARY

                st.subheader("📋 Meeting Summary")

                summary = result.get("summary", "")

                if summary:

                    st.write(summary)

                else:

                    st.info("No meeting summary was generated.")


                st.divider()

                # ACTION ITEMS

                st.subheader("✅ Action Items")

                action_items = result.get("action_items", [])

                if action_items:

                    action_data = []

                    for item in action_items:

                        action_data.append({
                            "Task": item.get(
                                "task",
                                "Not specified"
                            ),
                            "Owner": item.get(
                                "owner",
                                "Not specified"
                            ),
                            "Deadline": item.get(
                                "deadline",
                                "Not specified"
                            )
                        })

                    action_df = pd.DataFrame(action_data)

                    st.dataframe(
                        action_df,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No action items were identified in this meeting."
                    )


                st.divider()

                # PRIORITY CLASSIFICATION

                st.subheader("⚡ Priority Classification")

                priority_items = result.get("priority", [])

                if priority_items:

                    priority_data = []

                    for item in priority_items:

                        priority_data.append({
                            "Task": item.get(
                                "task",
                                "Not specified"
                            ),
                            "Owner": item.get(
                                "owner",
                                "Not specified"
                            ),
                            "Deadline": item.get(
                                "deadline",
                                "Not specified"
                            ),
                            "Priority": item.get(
                                "priority",
                                "Not specified"
                            )
                        })

                    priority_df = pd.DataFrame(priority_data)

                    st.dataframe(
                        priority_df,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No priority classification was required "
                        "because no action items were identified."
                    )


                st.divider()

                # ANALYSIS COMPLETE

                st.success(
                    "✓ Analysis complete"
                )


            except Exception as e:

                st.error(
                    "An error occurred while analyzing the meeting."
                )

                st.exception(e)