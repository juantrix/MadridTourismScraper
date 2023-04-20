import re
from sqlalchemy.orm import sessionmaker
from ..db.database import Category, engine


def has_html_tags(text):
    html_tags_re = re.compile(r'<[^>]+>')
    return bool(html_tags_re.search(text))


def test_category_descriptions_have_no_html():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if has_html_tags(category.description):
            errors.append(category)

    assert not errors, f"{len(errors)} categories have HTML in their description"


def test_category_descriptions_end_with_period():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if not category.description.endswith('.'):
            errors.append(category)

    assert not errors, f"{len(errors)} categories have no period at the end of their description"


def test_category_descriptions_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if category.description == '':
            errors.append(category)

    assert not errors, f"{len(errors)} categories have an empty description"


def test_category_names_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if category.name == '':
            errors.append(category)

    assert not errors, f"{len(errors)} categories have an empty name"


def test_category_images_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if category.image == '':
            errors.append(category)

    assert not errors, f"{len(errors)} categories have an empty image"


def test_category_images_are_valid():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if not category.image.startswith('http'):
            errors.append(category)

    assert not errors, f"{len(errors)} categories have an invalid image"


def test_category_names_are_unique():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if categories.count(category) > 1:
            errors.append(category)

    assert not errors, f"{len(errors)} categories have the same name"


def test_category_description_striped():
    Session = sessionmaker(bind=engine)
    session = Session()
    categories = session.query(Category).all()

    errors = []
    for category in categories:
        if category.description != category.description.strip():
            errors.append(category)

    assert not errors, f"{len(errors)} categories have a description with leading or trailing spaces"