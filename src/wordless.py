import click
import parser as p

@click.command()
@click.argument('filename')
def runAxion(filename):
    """Run axion script"""
    p.loadAndRunFile(filename, [{}])

if __name__ == "__main__":
    runAxion()
