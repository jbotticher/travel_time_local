from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL, Engine
from sqlalchemy import create_engine, Table, MetaData, Column
from sqlalchemy.dialects import postgresql
from jinja2 import Environment, FileSystemLoader, Template
from sqlalchemy import inspect



def transform(engine: Engine, sql_template: Template, table_name: str):
    extract_type = sql_template.make_module().config.get("extract_type")

    if extract_type == "full":
        full_sql = f"""
        drop table if exists {table_name};
        create table {table_name} as (
        {sql_template.render()}
        )"""
        engine.execute(full_sql)
    elif extract_type == "incremental":
        # source_table_name = sql_template.make_module().config.get("source_table_name")
        if inspect(engine).has_table(table_name):
            incremental_column = sql_template.make_module().config.get(
                "incremental_column"
            )
            sql_result = [
                dict(row)
                for row in engine.execute(
                    f"select max({incremental_column}) as incremental_value from {table_name}"
                ).all()
            ]
            incremental_value = sql_result[0].get("incremental_value")
            inc_sql = sql_template.render(
                is_incremental=True, incremental_value=incremental_value
            )
        else:
            inc_sql = sql_template.render(is_incremental=False)

        insert_sql = f"""
        insert into {table_name} (
        {inc_sql}
        )"""
        print(insert_sql)
        engine.execute(insert_sql)
    else:
        raise Exception(
            f"Extract type {extract_type} is not supported. Please use either 'full' or 'incremental' extract type."
    )





if __name__ == "__main__":
    load_dotenv()

    TARGET_DATABASE_NAME = os.environ.get("DATABASE_NAME")
    TARGET_SERVER_NAME = os.environ.get("SERVER_NAME")
    TARGET_DB_USERNAME = os.environ.get("DB_USERNAME")
    TARGET_DB_PASSWORD = os.environ.get("DB_PASSWORD")
    TARGET_PORT = os.environ.get("PORT")

    target_connection = URL.create(
        drivername = "postgresql+pg8000",
        username = TARGET_DB_USERNAME,
        password = TARGET_DB_PASSWORD,
        host = TARGET_SERVER_NAME,
        port = TARGET_PORT,
        database = TARGET_DATABASE_NAME
    )
    engine = create_engine(target_connection)


    transform_env = Environment(loader=FileSystemLoader("project/sql/transform"))
    transform_table_name = "travel_time_transform"
    transform_sql_template = transform_env.get_template(
        f"{transform_table_name}.sql"
    )

    transform(
        engine = engine,
        sql_template = transform_sql_template,
        table_name = transform_table_name
    )



