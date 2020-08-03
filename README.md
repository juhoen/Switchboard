# Switchboard for Python

[![PyPI](https://img.shields.io/pypi/v/python-switchboard?label=python-switchboard)](https://pypi.org/project/python-switchboard/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Switchboard makes working with API's easy. Switchboard helps you can easily convert JSON schemas. By creating a switchboard and defining some cords, you can manage which fields of the old schema implies to which fields in the new schema.

![Switchboard operator](https://live.staticflickr.com/7178/7120934237_e7e2e07eeb_c.jpg)

The name Switchboard is an association of old time telephone operators. By using the Switchboard, you act as the operator. Linking schema fields to each other resembles a telephone operator's switchboard. Photo by [Gawler History](https://www.flickr.com/photos/gawler_history/).

## But why Switchboard?

When working with integrations and 3rd party API's, for instance, you often run into situation where the data must be digged manually. Let us consider that you have the following kind of simple database schema:

```
 Column        | Type
---------------+-------
 first_name    | string
 last_name     | string
 email         | string

```

You are working with 3rd party user API, for instance, which returns the following kind of payload:

```json
{
  "id": 12335,
  "firstName": "John",
  "lastName": "Doe",
  "contactInfo": {
    "primaryEmail": "john.doe@foo.bar"
  }
}
```

So, what to do now? What is the best way to convert payload into your own format? Does this look familiar:

```py
response_dict = json.loads(response.body)

data = {
    "first_name": response_dict.get("firstName"),
    "last_name": response_dict.get("lastName"),
    "email": response_dict.get("contactInfo", {}).get("primaryEmail")
}
```

Unfortunately, the solution above becomes extremely messy when working with nested JSON structures, multiple 3rd party API's, or combination of them. This is why Switchboard is useful, by defining a new switchboard, you can easily manage data mappings between differen schemas.

```py
from switchboard import Switchboard, Cord

class UserSwitchboard(Switchboard):
    first_name = Cord("firstName")
    last_name = Cord("lastName")
    email = Cord(["contactInfo", "primaryEmail"])  # Notice how simple it is to access nested data!
```

Now, the code looks much better. Nice!

```py
response_dict = json.loads(response.body)
data = UserSwitchboard().apply(response_dict)
```

## Documentation

_This project is still in progress. Better documentation is coming later._

Defining new Switchboards is easy. All you need to do is to import it, and define some chords.

```py
from switchboard import Switchboard, Cord

class MySwitchboard(Switchboard):
    pet_name = Cord(
        source="petName",  # Source tells field location in source schema
        required=True,     # If field is required and missing, exception is raised
        default="Mr. Dog"  # If field is missing, default value is being used
    )
```

### Meta class

Switchboard functionality can be tweaked using Meta class:

```py
from switchboard import Switchboard, Cord

class MySwitchboard(Switchboard):
    class Meta:
        # Tells what to do with missing fields. Default functionlity is INCLUDE,
        # which means that if source field is missing, field is appended but the field
        # value will be None
        missing = Switchboard.EXCLUDE  # Options: Switchboard.EXCLUDE | Switchboard.INCLUDE | Switchboard.RAISE

    pet_name = Cord("petName")
```

### Nested schemas

Cords can access nested fields, even lists.

```py
from switchboard import Switchboard, Cord

class MySwitchboard(Switchboard):
    target_field = Cord(
        source=[
            "field1",  # Matches to field key
            0,         # Matches to list index
            "field2"   # Matches to field key
        ]
    )

MySwitchboard().apply({ "field1": [{ "field2": "value" }] })
# > { "target_field": "value" }
```

### Lists

Switchboard `many` attribute helps with dealing with lists. For example:

```py
class MySwitchboard(Switchboard):
    target = Cord("source")


data_in = [
    {"source": 1},
    {"source": 2},
    {"source": 3},
    {"source": 4}
]

MySwitchboard(many=True).apply(data_in)
# > { "target": 1, "target": 2, "target": 3, "target": 4 }

```
