:warning: WORK IN PROGRESS :warning:

# Python Switchboard

Switchboard makes working with API's easy. With Switchboard, you can easily convert JSON-objects.

## Switchboard object

Let's assume we have to following kind of data structure
```py
{
  "pet_name": "Mr. Dog",
  "legs": {
    "count": 4
  }
}
```

By defining a new Switchboard ...

```py
from switchboard import Switchboard, wires

PetSwitchboard(Switchboard):
   name = wires.StreamWire(source="pet_name")
   leg_count = wires.StreamWire(source=["legs", "count"], default=4)
```

... and applying it ...

```py
PetSwitchboard().apply(data_in)
```

... we can easily convert data format.

```py
{
  "name": "Mr. Dog",
  "leg_count": 4
}

```

This becomes really handly, when working with multiple data provides, integrations, etc...

## UP NEXT
- `many` attribute for Switchboards in order to convert lists of objects
- Support for nested Switchboards
- Proper documentation
