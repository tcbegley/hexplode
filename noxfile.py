import nox

nox.options.sessions = ["lint", "test"]

SOURCES = ["src", "tests", "noxfile.py"]


@nox.session
def lint(session):
    """Lint Python source"""
    session.install("black", "flake8", "isort", "mypy>=0.800")
    session.run("black", "--check", *SOURCES)
    session.run("flake8", *SOURCES)
    session.run("isort", "--check", *SOURCES)
    session.run("mypy", *SOURCES)


@nox.session(name="format")
def format_(session):
    session.install("black", "isort")
    session.run("black", *SOURCES)
    session.run("isort", *SOURCES)


@nox.session(python=["3.9"])
def test(session):
    """Run tests"""
    session.install("poetry")
    env = {"VIRTUAL_ENV": session.virtualenv.location}
    session.run("poetry", "install", "--no-dev", env=env, external=True)
    session.install("pytest")
    session.run("pytest")
