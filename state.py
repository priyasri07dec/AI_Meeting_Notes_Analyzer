from typing import TypedDict, List, Dict

class MeetingState(TypedDict):
    transcript : str
    topics : List[str]
    summary : str
    action_items: List[Dict[str, str]]
    priority : List[Dict[str, str]]
    final_report : str