import tempfile
from pathlib import Path
from typing import Any

import pytest
import yaml

from template_pipeline.configuration import load_job_configuration


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_JOB_FILE = PROJECT_ROOT / "configs/jobs/example.yaml"


def test_loads_example_job() -> None:
    configuration = load_job_configuration(EXAMPLE_JOB_FILE)

    assert configuration["job"]["name"] == "example"
    assert configuration["spark"]["executors"]["instances"] == 2
    assert configuration["output"]["format"] == "hudi"


def test_rejects_missing_output() -> None:
    job_data = _load_example_job_data()
    del job_data["output"]

    with pytest.raises(
        ValueError,
        match="Missing required field 'output'",
    ):
        _load_temporary_job(job_data)


def test_rejects_non_positive_executor_instances() -> None:
    job_data = _load_example_job_data()
    job_data["spark"]["executors"]["instances"] = 0

    with pytest.raises(
        ValueError,
        match="spark.executors.instances.*greater than zero",
    ):
        _load_temporary_job(job_data)


def test_rejects_string_executor_instances() -> None:
    job_data = _load_example_job_data()
    job_data["spark"]["executors"]["instances"] = "2"

    with pytest.raises(
        TypeError,
        match="spark.executors.instances.*integer",
    ):
        _load_temporary_job(job_data)


def test_rejects_boolean_executor_instances() -> None:
    job_data = _load_example_job_data()
    job_data["spark"]["executors"]["instances"] = True

    with pytest.raises(
        TypeError,
        match="spark.executors.instances.*integer",
    ):
        _load_temporary_job(job_data)


def test_rejects_invalid_yaml() -> None:
    with tempfile.TemporaryDirectory() as directory:
        job_file = Path(directory) / "job.yaml"
        job_file.write_text("job: [invalid", encoding="utf-8")

        with pytest.raises(yaml.YAMLError):
            load_job_configuration(job_file)


def test_rejects_non_mapping_root() -> None:
    with pytest.raises(
        TypeError,
        match="configuration.*mapping",
    ):
        _load_temporary_job(["job", "spark", "output"])


def _load_example_job_data() -> dict[str, Any]:
    return yaml.safe_load(EXAMPLE_JOB_FILE.read_text(encoding="utf-8"))


def _load_temporary_job(job_data: Any) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as directory:
        job_file = Path(directory) / "job.yaml"
        job_file.write_text(
            yaml.safe_dump(job_data),
            encoding="utf-8",
        )

        return load_job_configuration(job_file)
