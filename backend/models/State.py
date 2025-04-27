from typing_extensions import TypedDict


class State(TypedDict):
    """
    Similar to a Data Transfer Object (DTO), but with a more specific purpose.
    This class represents the state of a user query throughout the different pipline stages
    """
    question: str
    sql_query: str
    sql_result: str
    answer: str
    relevant_tables: list

