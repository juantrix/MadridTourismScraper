import re
from sqlalchemy.orm import sessionmaker
from ..db.database import Itinerary, engine


def has_html_tags(text):
    html_tags_re = re.compile(r'<[^>]+>')
    return bool(html_tags_re.search(text))


def test_itinerary_descriptions_have_no_html():
    Session = sessionmaker(bind=engine)
    session = Session()
    itineraries = session.query(Itinerary).all()

    errors = []
    for itinerary in itineraries:
        if has_html_tags(itinerary.description):
            errors.append(itinerary)

    assert not errors, f"{len(errors)} itineraries have HTML in their description"


def test_itinerary_descriptions_end_with_period():
    Session = sessionmaker(bind=engine)
    session = Session()
    itineraries = session.query(Itinerary).all()

    errors = []
    for itinerary in itineraries:
        if not itinerary.description.endswith('.'):
            errors.append(itinerary)

    assert not errors, f"{len(errors)} itineraries have no period at the end of their description"


def test_itinerary_descriptions_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    itineraries = session.query(Itinerary).all()

    errors = []
    for itinerary in itineraries:
        if itinerary.description == '':
            errors.append(itinerary)

    assert not errors, f"{len(errors)} itineraries have an empty description"


def test_itinerary_names_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    itineraries = session.query(Itinerary).all()

    errors = []
    for itinerary in itineraries:
        if itinerary.name == '':
            errors.append(itinerary)

    assert not errors, f"{len(errors)} itineraries have an empty name"


def test_itinerary_images_are_not_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    itineraries = session.query(Itinerary).all()

    errors = []
    for itinerary in itineraries:
        if itinerary.image == '':
            errors.append(itinerary)

    assert not errors, f"{len(errors)} itineraries have an empty image"


def test_itinerary_images_are_valid():
    Session = sessionmaker(bind=engine)
    session = Session()
    itineraries = session.query(Itinerary).all()

    errors = []
    for itinerary in itineraries:
        if not itinerary.image.startswith('http'):
            errors.append(itinerary)

    assert not errors, f"{len(errors)} itineraries have an invalid image"


def test_itinerary_description_striped():
    Session = sessionmaker(bind=engine)
    session = Session()
    itineraries = session.query(Itinerary).all()

    errors = []
    for itinerary in itineraries:
        if itinerary.description.strip() != itinerary.description:
            errors.append(itinerary)

    assert not errors, f"{len(errors)} itineraries have an invalid description"