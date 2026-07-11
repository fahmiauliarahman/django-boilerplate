import argparse
import keyword
from pathlib import Path

from django.core.management import call_command


parser = argparse.ArgumentParser(description="Create a package-based Django module")
parser.add_argument("name")
args = parser.parse_args()

name = args.name
if not name.isidentifier() or keyword.iskeyword(name):
    parser.error("name must be a valid Python identifier")

destination = Path("modules") / name
if destination.exists():
    parser.error(f"{destination} already exists")

destination.mkdir(parents=True)
call_command("startapp", name, destination)

apps_file = destination / "apps.py"
apps_file.write_text(
    apps_file.read_text().replace(f"name = '{name}'", f'name = "modules.{name}"')
)

for package in ("admin", "models", "tests", "views"):
    (destination / f"{package}.py").unlink()
    package_dir = destination / package
    package_dir.mkdir()
    (package_dir / "__init__.py").touch()

print(f"Created Django module: modules.{name}")
