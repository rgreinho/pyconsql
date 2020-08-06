import os
from pathlib import Path

from invoke import task

PROJECT = Path(".").absolute().name


@task
def format(c, write=False):
    """Format the codebase."""
    write_or_diff = "" if write else "--check"
    c.run(f"poetry run black {write_or_diff} .")


@task
def lint(c):
    """Lint the codebase."""
    c.run(f"poetry run pylint {PROJECT}")
    c.run(f"poetry run flake8 {PROJECT}")


@task
def check(c):
    """Run the static analyzers."""
    c.run(f"poetry run pydocstyle {PROJECT}")


@task
def docs(c):
    """Build the documentation."""
    with c.cd("docs"):
        c.run("poetry run make html")


@task
def test(c):
    """Run the unit tests."""
    test_report_dir = os.environ.get("CIRCLE_TEST_REPORTS", "/tmp")
    c.run(
        "poetry run pytest -x "
        f"--junitxml={test_report_dir}/pytest/junit.xml "
        "--cov-report term-missing "
        "--cov-report html "
        f"--cov={PROJECT} "
    )


@task(format, lint, check, docs, test)
def ci(c):
    """Run all the CI tasks at once."""


@task
def publish_packages(c):
    """Publish packages on our internal PyPI."""
    c.run(
        "poetry publish --repository shipstation "
        f"--password {os.environ.get('GITHUB_TOKEN')}"
    )


@task
def local_api(c):
    """Run Connexion locally."""
    c.run(
        "poetry run gunicorn "
        "--reload "
        "--timeout 1800 "
        "--log-level debug "
        "-b 0.0.0.0:8000 "
        "--worker-class aiohttp.GunicornUVLoopWebWorker "
        f"{PROJECT}.wsgi",
        env={"CONNEXION_SETTINGS_MODULE": f"{PROJECT}.api.settings.local"},
    )


@task
def cleanup(c):
    c.run("rm -fr ./alembic/versions/*")
    c.run("rm -fr petstore.db")


@task
def migrate(c):
    """Apply migrations."""
    c.run("poetry run alembic upgrade head")


@task
def migrations(c, message):
    """Make new migrations."""
    migration_dir = Path("alembic/versions/")
    migration_count = len(list(migration_dir.glob("*.py")))
    c.run(
        "poetry run alembic revision --autogenerate "
        f'--rev-id={migration_count:04d} -m "{message}"'
    )
