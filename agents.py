from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL
from state import MeetingState

client = genai.Client(api_key=GEMINI_API_KEY)

def topic_extraction_agent(state: MeetingState) -> MeetingState:
    """
    Extract the main discussion topics from the meeting transcript.
    """

    transcript = state["transcript"]

    prompt = f"""
You are a Meeting Topic Extraction Agent.

Read the following meeting transcript and identify the main discussion
topics.

Rules:
- Return only the important topics discussed.
- Do not include explanations.
- Do not invent topics that are not present in the transcript.
- Return the topics as a numbered list.

Meeting Transcript:
{transcript}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    topics_text = response.text.strip()

    topics = []

    for line in topics_text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Remove common numbering formats such as:
        # 1. Topic
        # 2) Topic
        # - Topic
        if "." in line[:3]:
            line = line.split(".", 1)[1].strip()

        elif ")" in line[:3]:
            line = line.split(")", 1)[1].strip()

        elif line.startswith("-"):
            line = line[1:].strip()

        topics.append(line)

    return {
        **state,
        "topics": topics
    }

def meeting_summary_agent(state: MeetingState) -> MeetingState:
    """
    Generate a concise summary of the meeting.
    """

    transcript = state["transcript"]

    prompt = f"""
You are a Meeting Summary Agent.

Read the following meeting transcript and generate a concise summary.

Rules:
- Write exactly 3 to 5 sentences.
- Explain the main purpose of the meeting.
- Mention the important discussions and decisions.
- Mention important tasks or deadlines when relevant.
- Do not invent information.
- Do not use bullet points.
- Return only the summary.

Meeting Transcript:
{transcript}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    summary = response.text.strip()

    return {
        **state,
        "summary": summary
    }

def action_item_agent(state: MeetingState) -> MeetingState:
    """
    Extract explicit action items, owners, and deadlines.
    """

    transcript = state["transcript"]

    prompt = f"""
You are an Action Item Extraction Agent.

Read the meeting transcript carefully and identify all explicit
actionable tasks.

For every action item, identify:
1. Task
2. Owner
3. Deadline

IMPORTANT DEADLINE RULES:

1. If a task has its own explicit deadline stated with or immediately
   associated with the task, preserve that deadline.

2. Do NOT replace a task-specific deadline with a later general
   deadline.

3. A later deadline may be applied to an action item ONLY when that
   action item does not already have its own specific deadline.

4. If a later statement clearly applies to multiple tasks, assign
   that deadline only to the tasks that do not already have a
   task-specific deadline.

Example:

David: I will complete Task A this week.
Sarah: I will complete Task B.
John: Both tasks must be completed before Friday.

Correct result:

Task: Task A
Owner: David
Deadline: This week

Task: Task B
Owner: Sarah
Deadline: Before Friday

Do NOT change Task A's "This week" deadline to "Before Friday".

Rules:
- Extract only explicit actionable tasks.
- Do not invent tasks.
- Do not convert general discussion into action items.
- Do not treat "we will discuss this in the next meeting" as an
  action item.
- If a genuine action item has no named owner, use exactly:
  "Not specified".
- If no deadline is stated or reasonably associated with the task,
  use exactly:
  "Not specified".
- Preserve the meaning of task-specific deadlines.
- If there are no genuine action items, return exactly:
  NO_ACTION_ITEMS

Use exactly this format:

Task: <task>
Owner: <owner>
Deadline: <deadline>

Meeting Transcript:
{transcript}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    action_items_text = response.text.strip()

    if action_items_text.upper() == "NO_ACTION_ITEMS":
        return {
            **state,
            "action_items": []
        }

    action_items = []

    current_task = None
    current_owner = None
    current_deadline = None

    for line in action_items_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.lower().startswith("task:"):
            current_task = line.split(":", 1)[1].strip()

        elif line.lower().startswith("owner:"):
            current_owner = line.split(":", 1)[1].strip()

        elif line.lower().startswith("deadline:"):
            current_deadline = line.split(":", 1)[1].strip()

            if current_task:
                action_items.append({
                    "task": current_task,
                    "owner": current_owner or "Not specified",
                    "deadline": current_deadline or "Not specified"
                })

                current_task = None
                current_owner = None
                current_deadline = None

    return {
        **state,
        "action_items": action_items
    }

def priority_classification_agent(state: MeetingState) -> MeetingState:
    """
    Classify action items according to their deadline and urgency.
    """

    action_items = state["action_items"]

    if not action_items:
        return {
            **state,
            "priority": []
        }

    priority_items = []

    for item in action_items:

        task = item["task"]
        owner = item["owner"]
        deadline = item["deadline"]

        deadline_lower = deadline.lower()

        # High Priority
        if any(keyword in deadline_lower for keyword in [
            "urgent",
            "asap",
            "today",
            "immediately",
            "by tomorrow",
            "tomorrow"
        ]):
            priority = "High Priority"

        # Medium Priority
        elif any(keyword in deadline_lower for keyword in [
            "this week",
            "before friday",
            "this month",
            "upcoming"
        ]):
            priority = "Medium Priority"

        # Low Priority
        else:
            priority = "Low Priority"

        priority_items.append({
            "task": task,
            "owner": owner,
            "deadline": deadline,
            "priority": priority
        })

    return {
        **state,
        "priority": priority_items
    }

def final_output_agent(state: MeetingState) -> MeetingState:
    """
    Combine all meeting analysis results into a final structured report.
    """

    topics = state["topics"]
    summary = state["summary"]
    action_items = state["action_items"]
    priority_items = state["priority"]

    report = "===== MEETING ANALYSIS =====\n\n"

    report += "KEY TOPICS\n"
    for topic in topics:
        report += f"- {topic}\n"

    report += "\nMEETING SUMMARY\n"
    report += f"{summary}\n"

    report += "\nACTION ITEMS\n"

    if not action_items:
        report += "No action items identified.\n"

    else:
        for item in action_items:
            report += f"- Task: {item['task']}\n"
            report += f"  Owner: {item['owner']}\n"
            report += f"  Deadline: {item['deadline']}\n"

    if priority_items:
        report += "\nPRIORITY\n"

        for item in priority_items:
            report += f"- Task: {item['task']}\n"
            report += f"  Owner: {item['owner']}\n"
            report += f"  Deadline: {item['deadline']}\n"
            report += f"  Priority: {item['priority']}\n"

    return {
        **state,
        "final_report": report
    }