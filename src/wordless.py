import click
import parser as p

@click.command()
@click.argument('filename')
def runWordless(filename):
    """Run wordless script"""
    p.loadAndRunFile(filename, [{}])

if __name__ == "__main__":
    runWordless()
