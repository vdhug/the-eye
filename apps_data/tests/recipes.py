# Third-party app imports
from model_bakery.recipe import Recipe as mommy_recipe, foreign_key
from datetime import datetime
from uuid import UUID

from apps_data.models import Application, Session, Event


# Application mommy recipes
application_mommy_recipe = mommy_recipe(
    Application,
    name="Web App",
)

# Session mommy recipes
session_mommy_recipe = mommy_recipe(
    Session,
    application=foreign_key(application_mommy_recipe),
    uuid=UUID("e2085be5-9137-4e4e-80b5-f1ffddc25423"),
)

# Event mommy recipes
event_mommy_recipe = mommy_recipe(
    Event,
    session=foreign_key(session_mommy_recipe),
    name="submit",
    category="form interaction",
    payload={
        "host": "www.consumeraffairs.com",
        "path": "/",
        "form": {"first_name": "John", "last_name": "Doe"},
    },
    timestamp=datetime.strptime("2021-01-01 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"),
)
