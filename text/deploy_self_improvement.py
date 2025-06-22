def process_data(data):
    try:
        result = []
        for record in data:
            if len(record) != 3:
                raise ValueError("Each record must have exactly 3 elements.")
            id_, name, value = record
            if not isinstance(id_, int) or id_ < 0:
                raise ValueError(f"ID {id_} is not a valid ID.")
            if not isinstance(name, str) or len(name.strip()) == 0:
                raise ValueError(f"Name '{name}' is not a valid name.")
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"Value {value} is not a valid value.")
            result.append((id_, name, value))
        return result
    except ValueError as e:
        print(f"Error processing data: {e}", flush=True)
        return None