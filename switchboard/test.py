import wires
from switchboard import Switchboard, INCLUDE


data = {
    "kissa": "Mirri",
    "koira": "Musti",
    "papukaija": [{
        "nimi": "Pörrö"
    }]
}


class PetSwitchboard(Switchboard):

    class Meta:
        missing = INCLUDE

    cat = wires.StreamWire(source="kissa")
    dog = wires.StreamWire(source="koira")
    parrot = wires.StreamWire(source=["papukaija", 1, "nimi"])


print(PetSwitchboard().apply(data))
