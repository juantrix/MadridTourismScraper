import re
from sqlalchemy.orm import sessionmaker
from ..db.database import Route, engine


def has_html_tags(text):
    html_tags_re = re.compile(r'<[^>]+>')
    return bool(html_tags_re.search(text))


def test_route_descriptions_have_no_html():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if has_html_tags(route.description):
            errors.append(route)

    assert not errors, f"{len(errors)} routes have HTML in their description"


def test_route_descriptions_end_with_period():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if not route.description.endswith('.'):
            errors.append(route)

    assert not errors, f"{len(errors)} routes have no period at the end of their description" 


def test_route_descriptions_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if route.description == '':
            errors.append(route)

    assert not errors, f"{len(errors)} routes have an empty description"


def test_route_names_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if route.name == '':
            errors.append(route)

    assert not errors, f"{len(errors)} routes have an empty name"


def test_route_names_are_not_none():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if route.name is None:
            errors.append(route)

    assert not errors, f"{len(errors)} routes have a None name"


def test_route_descriptions_are_not_none():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if route.description is None:
            errors.append(route)

    assert not errors, f"{len(errors)} routes have a None description"


def test_route_images_are_valid():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if not route.image.startswith('http'):
            errors.append(route)

    assert not errors, f"{len(errors)} routes have a invalid image"


def test_route_description_striped():
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = session.query(Route).all()

    errors = []
    for route in routes:
        if route.description.strip() != route.description:
            errors.append(route)

    assert not errors, f"{len(errors)} routes have a description with leading or trailing spaces"