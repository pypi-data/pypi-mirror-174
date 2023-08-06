
import click

"python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ --skip-existing  dist/archimedean-0.0.1.macosx-10.9-universal2.tar.gz"

@click.command()
def test():
    print("Hello World")
    print("Hello")
