from langgraph.graph import StateGraph, START, END

from state import MeetingState

from agents import (
    topic_extraction_agent,
    meeting_summary_agent,
    action_item_agent,
    priority_classification_agent,
    final_output_agent
)


def route_after_action_items(state: MeetingState) -> str:
    """
    Decide whether the Priority Agent should run.
    """

    if state["action_items"]:
        return "priority"

    return "final_output"


# Create the graph
builder = StateGraph(MeetingState)


# Add agents as nodes
builder.add_node(
    "topic_extraction",
    topic_extraction_agent
)

builder.add_node(
    "meeting_summary",
    meeting_summary_agent
)

builder.add_node(
    "action_items",
    action_item_agent
)

builder.add_node(
    "priority",
    priority_classification_agent
)

builder.add_node(
    "final_output",
    final_output_agent
)


# Normal workflow
builder.add_edge(
    START,
    "topic_extraction"
)

builder.add_edge(
    "topic_extraction",
    "meeting_summary"
)

builder.add_edge(
    "meeting_summary",
    "action_items"
)


# Conditional routing
builder.add_conditional_edges(
    "action_items",
    route_after_action_items,
    {
        "priority": "priority",
        "final_output": "final_output"
    }
)


# After Priority Agent
builder.add_edge(
    "priority",
    "final_output"
)


# Final output
builder.add_edge(
    "final_output",
    END
)


# Compile the graph
meeting_graph = builder.compile()