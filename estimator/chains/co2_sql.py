from typing import Literal

from langchain.chains import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase

from estimator.prompt_templates.co2_sql_prompts import (
    DK_CO2_SQL_PROMPT_TEMPLATE,
    EN_CO2_SQL_PROMPT_TEMPLATE,
)


def get_en_co2_sql_chain(language: Literal["da", "en"], verbose: bool = False):
    sql_dk_co2_db = SQLDatabase.from_uri("sqlite:///estimator/data/dk_co2_emission.db", sample_rows_in_table_info=2)
    llm = ChatOpenAI(  # type: ignore
        temperature=0,
    )
    co2_sql_chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=sql_dk_co2_db,
        verbose=verbose,
        prompt=EN_CO2_SQL_PROMPT_TEMPLATE if language == "en" else DK_CO2_SQL_PROMPT_TEMPLATE,
        top_k=100,
    )

    return co2_sql_chain
