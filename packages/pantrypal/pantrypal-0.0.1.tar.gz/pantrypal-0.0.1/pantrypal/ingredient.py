class Ingredient:
    def __init__(self):
        self._name: str = None
        self._unit: str = None

    def __repr__(self):
        if self._name is not None:
            string = f"{self._name}"
        else:
            string = "PantryPal ingredient"
        return string
