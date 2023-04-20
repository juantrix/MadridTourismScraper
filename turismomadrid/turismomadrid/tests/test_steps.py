import re
from sqlalchemy.orm import sessionmaker
from ..db.database import Step, engine


def has_html_tags(text):
    html_tags_re = re.compile(r'<[^>]+>')
    return bool(html_tags_re.search(text))


def test_step_descriptions_have_no_html():
    Session = sessionmaker(bind=engine)
    session = Session()
    steps = session.query(Step).all()

    errors = []
    for step in steps:
        if has_html_tags(step.description):
            errors.append(step)

    assert not errors, f"{len(errors)} steps have HTML in their description"


def test_step_descriptions_end_with_period():
    Session = sessionmaker(bind=engine)
    session = Session()
    steps = session.query(Step).all()

    errors = []
    for step in steps:
        if not step.description.endswith('.'):
            errors.append(step)

    assert not errors, f"{len(errors)} steps have no period at the end of their description"


def test_step_descriptions_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    steps = session.query(Step).all()

    errors = []
    for step in steps:
        if step.description == '':
            errors.append(step)

    assert not errors, f"{len(errors)} steps have an empty description"


def test_step_names_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    steps = session.query(Step).all()

    errors = []
    for step in steps:
        if step.name == '':
            errors.append(step)

    assert not errors, f"{len(errors)} steps have an empty name"


def test_step_images_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    steps = session.query(Step).all()

    errors = []
    for step in steps:
        if step.image == '':
            errors.append(step)

    assert not errors, f"{len(errors)} steps have an empty image"


def test_step_images_are_valid():
    Session = sessionmaker(bind=engine)
    session = Session()
    steps = session.query(Step).all()

    errors = []
    for step in steps:
        if step.image is not None:
            if not step.image.startswith('http'):
                errors.append(step)

    assert not errors, f"{len(errors)} steps have an invalid image"


def test_step_description_striped():
    Session = sessionmaker(bind=engine)
    session = Session()
    steps = session.query(Step).all()

    errors = []
    for step in steps:
        if step.description != step.description.strip():
            errors.append(step)

    assert not errors, f"{len(errors)} steps have an invalid description"