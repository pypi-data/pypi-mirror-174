import pkg_resources

from os import system as sm


def freeze(requirements_file="requirements.txt"):
    sm(f"pip freeze > {requirements_file}")

def inspect():
    sm("pip inspect > inspect.txt")
    with open("inspect.txt") as file:
        inspect_result = file.read()
    sm("del inspect.txt")
    return inspect_result


def plist():
    return [p.project_name for p in pkg_resources.working_set]


def show(pkg_name):
    sm(f"pip show {pkg_name} > show.txt")
    show_result = {}
    with open("show.txt") as f:
        lines = f.read()[:-1].split("\n")
        for n in lines:
            show_result[n.split(":", 1)[0]] = n.split(":", 1)[1]
    sm("del show.txt")
    return show_result


def check():
    sm("pip check > check.txt")
    with open("check.txt") as f:
        return f.read()
