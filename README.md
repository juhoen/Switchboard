# Switchboard for Python

[![PyPI](https://img.shields.io/pypi/v/python-switchboard?label=python-switchboard)](https://pypi.org/project/python-switchboard/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Switchboard makes working with API's easy. Switchboard helps you can easily convert JSON schemas. Switchboard is still work on progress, but you are more than welcome to check it out!

## Install Switchboard

```sh
$ pip install python-switchboard
```

## But why Switchboard?

When working with integrations and 3rd party API's, for instance, you often run into situation where the data must be digged manually. Let us consider that you have the following kind of simple database schema:

```
 Column        | Type
---------------+-------
 first_name    | string
 last_name     | string
 email         | string

```

However, you are working with 3rd party user API, which returns the following kind of payload:

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

So, what now? What's the best way to convert payload into your format? Does this look familiar:

```py
response_dict = json.loads(response.body)

data = {
    "first_name": response_dict.get("firstName"),
    "last_name": response_dict.get("lastName"),
    "email": response_dict.get("contactInfo", {}).get("primaryEmail")
}
```

Unfortunately, the solution above becomes extremely messy when working with nested JSON structures, multiple 3rd party API's, or combination of them. This is why Switchboard is useful. By defining a new switchboard, you can easily manage data mappings between different schemas.

```py
from switchboard import Switchboard, Wire

class UserSwitchboard(Switchboard):
    first_name = Wire("firstName")
    last_name = Wire("lastName")
    email = Wire(["contactInfo", "primaryEmail"])  # Notice how simple it is to access nested data!
```

The code looks much better now. Nice!

```py
response_dict = json.loads(response.body)
data = UserSwitchboard().apply(response_dict)
```

## Documentation

_Switchboard is still in progress. Better documentation is coming later._

Defining new Switchboards is easy. All you need to do is to import `Switchboard`, and define some `Cord`s.

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

Switchboard's functionality can be tweaked using Meta class:

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
