def input_numeric(name: str) -> int:
    input_value: str = input(f"Input {name}")
    while not str.isnumeric(input_value):
        input_value = input(f"{name} must be numeric value")
    return int(input_value)
