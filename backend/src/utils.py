import re

def clean_sql_input(raw_sql: str) -> str:
    """
    Cleans copy-pasted SQL:
    - Removes leading bullets (+, -, *, etc.) or numbers with dot (1., 2., etc.)
    - Keeps normal SQL lines intact
    """
    cleaned_lines = []
    for line in raw_sql.splitlines():
        stripped = line.lstrip()

        # Only remove bullets/numbers if the line starts with them
        # Ignore lines that start with SQL keywords or *, etc.
        if re.match(r'^[\+\-\*]\s+', stripped):
            line = re.sub(r'^[\+\-\*]\s+', '', stripped)
        elif re.match(r'^\d+\.\s+', stripped):
            line = re.sub(r'^\d+\.\s+', '', stripped)
        else:
            # keep the line as-is
            line = line

        if line.strip():  # keep non-empty
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)