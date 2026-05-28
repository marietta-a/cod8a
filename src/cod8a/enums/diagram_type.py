from enum import Enum

class DiagramType(Enum):
    CLASS = "class"
    SEQUENCE = "sequence"
    FLOWCHART = "flowchart"
    USE_CASE = "use_case"
    ACTIVITY = "activity"
    COMPONENT = "component"
    DEPLOYMENT = "deployment"