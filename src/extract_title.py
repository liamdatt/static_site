def extract_title(markdown):
    lines_split = markdown.split("\n")
    for line in lines_split:
        if len(line) > 2:
            line = line.strip()
            if line[0:2] == "# ":
                return line[2:].strip()
    raise Exception("no h1 header found")
