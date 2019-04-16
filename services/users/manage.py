# services/users/manage.py


import unittest

from flask.cli import FlaskGroup

from project import create_app, db # new
from project.api.models import User # new

app = create_app() # new
cli = FlaskGroup(create_app=create_app) # new


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Ejecutar los tests sin covertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()