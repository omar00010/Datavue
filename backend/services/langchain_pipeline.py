from langchain_community.utilities import SQLDatabase
from langchain import hub
import models.State as State
from typing_extensions import TypedDict
from typing_extensions import Annotated
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()




class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]


class LangChainPipeline:
    """
    This class is responsible for the LangChain pipeline.
    It uses the LangChain library to generate SQL queries and fetch answers from the database.
    """

    def __init__(self):
        # Pull the query prompt template from LangChain hub
        self.query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
        self.query_prompt_template.messages[0].prompt.template = """

                ================================ System Message ================================

                Given an input question, create a syntactically correct {dialect} query to run to help find the answer. Unless the user specifies in his question a specific number of examples they wish to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

                Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

                Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

                Strictly use the table names and column names that you can see in the schema description. Do not use any other table or column name. If you are not sure about a table or column name, do not use it.
                        
                If you can not find a relevant table or column to answer the question, return "I don't know", include a reasoning.
                {table_info}

            """
        # Initialize the LLM with the API key
        self.llm = init_chat_model(
            "gpt-4o-mini",
            model_provider="openai",
            api_key=os.getenv("LANGCHAIN_API_KEY")
        )

    def write_sql_query(self, db, state: State):
        """Generate SQL query to fetch information."""
        # Prepare the prompt
        print("Relevant tables:", state["relevant_tables"])
        prompt = self.query_prompt_template.invoke(
            {
                "dialect": db.dialect,
                "top_k": 10,
                "table_info": state["relevant_tables"],
                "input": state["question"],
            }
        )

        # Use the structured output schema
        structured_llm = self.llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)

        # Update the state with the generated SQL query
        state["sql_query"] = result["query"]

        return state