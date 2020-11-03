import click
from jinja2 import Template, Environment, FileSystemLoader
import os

# consts
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@click.command()
@click.option("--mod-name", "-M", prompt="module name", default="default-app", help="Module name. Default is default-app.")
@click.option("--import-name", "-I", prompt="import name", default="app", help="Import name. Default is app.")
@click.option("--mod-version", "-V", prompt="version", default="1.0.0", help="Module version. Default is 1.0.0.")
@click.option("--description", "-D", prompt="description", default="Default application", help="Module description. Default is Default application.")
def execute(mod_name, import_name, mod_version, description):
    # input data
    data = {
        "mod_name": mod_name,
        "import_name": import_name,
        "mod_version": mod_version,
        "description": description
    }
    click.echo("Your application information is..")
    click.echo(data)
    env = Environment(loader=FileSystemLoader(f"{APP_ROOT}/pytemplate/resources"))

    click.echo("Create {mod_name} resources..")
    # setup.py
    setup_py = env.get_template("setup.py.j2")
    setup_py_render = setup_py.render(data)

    # setup.cfg
    setup_cfg = env.get_template("setup.cfg.j2")
    setup_cfg_render = setup_cfg.render(data)

    # app's __init__.py
    app_init_py = env.get_template("app.__init__.py.j2")
    app_init_py_render = app_init_py.render(data)

    # test's __init__.py
    test_init_py = env.get_template("test.__init__.py.j2")
    test_init_py_render = test_init_py.render(data)

    # tests.py
    tests_py = env.get_template("tests.py.j2")
    tests_py_render = tests_py.render(data)

    # application resources
    os.makedirs(f"./{mod_name}/{import_name}", exist_ok=True)
    # setup.py
    with open(f"./{mod_name}/setup.py", mode="w") as f:
        f.write(str(setup_py_render))
    # setup.cfg
    with open(f"./{mod_name}/setup.cfg", mode="w") as f:
        f.write(str(setup_cfg_render))
    # __init__.py
    with open(f"./{mod_name}/{import_name}/__init__.py", mode="w") as f:
        f.write(str(app_init_py_render))

    # tests resources
    os.makedirs(f"./{mod_name}/tests", exist_ok=True)
    # __init__.py
    with open(f"./{mod_name}/tests/__init__.py", mode="w") as f:
        f.write(str(test_init_py_render))
    # tests.py
    with open(f"./{mod_name}/tests/tests_{import_name}.py", mode="w") as f:
        f.write(str(tests_py_render))
    
    click.echo(f"Success! {mod_name} is created!")