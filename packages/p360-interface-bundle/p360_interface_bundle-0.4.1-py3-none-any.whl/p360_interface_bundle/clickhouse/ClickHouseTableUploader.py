import random
import string
from typing import Optional
from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from p360_interface_bundle.clickhouse.ClickHouseContext import ClickHouseContext
from p360_interface_bundle.clickhouse.ClickHouseQueryExecutor import ClickHouseQueryExecutor
from p360_interface_bundle.clickhouse.types import SPARK_TO_CLICKHOUSE_TYPES


class ClickHouseTableUploader:
    __engine_map = {
        "summing_merge_tree": "ENGINE = SummingMergeTree() ORDER BY {order_column} SETTINGS index_granularity = 8192",
        "aggregating_merge_tree": "ENGINE = AggregatingMergeTree() ORDER BY {order_column} SETTINGS index_granularity = 8192",
        "log": "ENGINE = Log",
    }

    def __init__(
        self,
        clickhouse_context: ClickHouseContext,
        clickhouse_query_executor: ClickHouseQueryExecutor,
    ):
        self.__clickhouse_context = clickhouse_context
        self.__clickhouse_query_executor = clickhouse_query_executor

    def upload_overwrite(self, df: DataFrame, table_name: str, engine_type: str, order_column: Optional[str] = None):
        self.__check_engine_type(engine_type, order_column)

        array_converted_df = self.__convert_arrays_to_strings(df)

        (
            array_converted_df.write.format("jdbc")
            .option("createTableOptions", self.__engine_map[engine_type].format(order_column=order_column))
            .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
            .option("url", f"jdbc:clickhouse://{self.__clickhouse_context.get_host()}:{self.__clickhouse_context.get_port()}")
            .option("dbtable", table_name)
            .option("user", self.__clickhouse_context.get_user())
            .option("password", self.__clickhouse_context.get_password())
            .mode("overwrite")
            .save()
        )

        self.__convert_strings_to_arrays(df, table_name, engine_type, order_column)  # pyre-ignore[6]

    def upload_append(self, df: DataFrame, table_name: str, engine_type: str, order_column: Optional[str] = None):
        self.__check_engine_type(engine_type, order_column)

        self.__clickhouse_query_executor.execute(f"DROP TABLE IF EXISTS {table_name}")

        array_converted_df = self.__convert_arrays_to_strings(df)

        create_table_query = self.__construct_create_table_query(
            array_converted_df, table_name, engine_type, order_column if order_column else ""
        )

        self.__clickhouse_query_executor.execute(create_table_query)

        (
            array_converted_df.write.format("jdbc")
            .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
            .option("url", f"jdbc:clickhouse://{self.__clickhouse_context.get_host()}:{self.__clickhouse_context.get_port()}")
            .option("dbtable", table_name)
            .option("user", self.__clickhouse_context.get_user())
            .option("password", self.__clickhouse_context.get_password())
            .mode("append")
            .save()
        )

        self.__convert_strings_to_arrays(df, table_name, engine_type, order_column)  # pyre-ignore[6]

    def __construct_create_table_query(self, df: DataFrame, table_name: str, engine_type: str, order_column: str) -> str:
        create_table_query = f"CREATE TABLE {table_name} ("
        clickhouse_columns = []

        for field in df.schema:
            col_name = field.name
            col_type = SPARK_TO_CLICKHOUSE_TYPES[field.dataType.simpleString()]

            if field.nullable and field.name != order_column:
                clickhouse_columns.append(f"`{col_name}` Nullable({col_type})")
            else:
                clickhouse_columns.append(f"`{col_name}` {col_type}")

        create_table_query += ", ".join(clickhouse_columns)
        create_table_query += ") "
        create_table_query += self.__engine_map[engine_type].format(order_column=order_column)

        return create_table_query

    def __check_engine_type(self, engine_type: str, order_column: Optional[str]):
        if engine_type not in self.__engine_map:
            raise Exception(f"Invalid engine type '{engine_type}', allowed types are {self.__engine_map.keys()}")

        if engine_type in ["summing_merge_tree", "aggregating_merge_tree"] and order_column is None:
            raise Exception(f"You must specify order column for engine type of '{engine_type}'")

    def __convert_arrays_to_strings(self, df: DataFrame) -> DataFrame:
        for field in df.schema.fields:
            if field.dataType.simpleString().startswith("array"):
                df = df.withColumn(field.name, f.concat_ws("`", field.name))

        return df

    def __convert_strings_to_arrays(self, df: DataFrame, table_name: str, engine_type: str, order_column: str):
        original_table = table_name
        converted_table = f"{table_name}_{''.join(random.choices(string.ascii_lowercase, k=6))}"

        create_table_query = f"CREATE TABLE {converted_table} "
        create_table_query += self.__engine_map[engine_type].format(order_column=order_column)
        create_table_query += " AS (SELECT "

        clickhouse_columns = []

        for field in df.schema.fields:
            if field.dataType.simpleString().startswith("array"):
                clickhouse_columns.append(
                    f"CAST(splitByChar('`', {field.name}) AS {SPARK_TO_CLICKHOUSE_TYPES[field.dataType.simpleString()]}) AS {field.name}"
                )
            else:
                clickhouse_columns.append(field.name)

        create_table_query += ", ".join(clickhouse_columns)
        create_table_query += f" FROM {original_table}"
        create_table_query += ")"

        self.__clickhouse_query_executor.execute(create_table_query)
        self.__clickhouse_query_executor.execute(f"DROP TABLE {original_table}")
        self.__clickhouse_query_executor.execute(f"RENAME TABLE {converted_table} TO {original_table}")
