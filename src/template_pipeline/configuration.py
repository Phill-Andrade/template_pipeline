from pathlib import Path
from typing import Any

import yaml


def load_job_configuration(file_path: Path) -> dict[str, Any]:
    content = file_path.read_text(encoding="utf-8")
    loaded_data = yaml.safe_load(content)
    configuration = _require_mapping_value(loaded_data, "configuration")

    validate_job_configuration(configuration)

    return configuration


def validate_job_configuration(configuration: dict[str, Any]) -> None:
    job = _require_mapping(configuration, "job", "job")
    spark = _require_mapping(configuration, "spark", "spark")
    _require_mapping(configuration, "output", "output")

    _require_string(job, "name", "job.name")
    _validate_spark_configuration(spark)


def _validate_spark_configuration(spark: dict[str, Any]) -> None:
    driver = _require_mapping(spark, "driver", "spark.driver")
    executors = _require_mapping(spark, "executors", "spark.executors")
    sql = _require_mapping(spark, "sql", "spark.sql")

    _validate_driver_resources(driver)
    _validate_executor_resources(executors)
    _require_positive_integer(
        sql,
        "shuffle_partitions",
        "spark.sql.shuffle_partitions",
    )


def _validate_driver_resources(driver: dict[str, Any]) -> None:
    _require_string(driver, "memory", "spark.driver.memory")
    _require_positive_integer(driver, "cores", "spark.driver.cores")


def _validate_executor_resources(executors: dict[str, Any]) -> None:
    _require_positive_integer(
        executors,
        "instances",
        "spark.executors.instances",
    )
    _require_string(executors, "memory", "spark.executors.memory")
    _require_positive_integer(
        executors,
        "cores",
        "spark.executors.cores",
    )


def _require_mapping(
    configuration: dict[str, Any],
    field: str,
    field_path: str,
) -> dict[str, Any]:
    value = _require_field(configuration, field, field_path)

    return _require_mapping_value(value, field_path)


def _require_mapping_value(
    value: Any,
    field_path: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"Field '{field_path}' must be a mapping.")

    return value


def _require_string(
    configuration: dict[str, Any],
    field: str,
    field_path: str,
) -> None:
    value = _require_field(configuration, field, field_path)

    if not isinstance(value, str):
        raise TypeError(f"Field '{field_path}' must be a string.")

    if not value.strip():
        raise ValueError(f"Field '{field_path}' cannot be empty.")


def _require_positive_integer(
    configuration: dict[str, Any],
    field: str,
    field_path: str,
) -> None:
    value = _require_field(configuration, field, field_path)

    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"Field '{field_path}' must be an integer.")

    if value <= 0:
        raise ValueError(f"Field '{field_path}' must be greater than zero.")


def _require_field(
    configuration: dict[str, Any],
    field: str,
    field_path: str,
) -> Any:
    if field not in configuration:
        raise ValueError(f"Missing required field '{field_path}'.")

    return configuration[field]
