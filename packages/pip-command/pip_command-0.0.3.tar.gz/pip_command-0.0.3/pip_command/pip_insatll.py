from os import system as sm


def install(lib_name, version=None):
    sm(f"pip install {lib_name + '==' + version if version else lib_name}")


def install_requirements(requirements_file_name):
    sm(f"pip install -r {requirements_file_name}")


def installs(*libs_name):
    sm(f"pip install {' '.join(libs_name)}")
    
    
def update(lib_name):
    sm(f"pip install -U {lib_name}")


def uninstall(lib_name):
    sm(f"pip uninstall -y {lib_name}")


def uninstall_requirements(requirements):
    sm(f"pip uninstall -y {requirements}")

