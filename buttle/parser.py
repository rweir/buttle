import shlex

def tokenise(line):
    """Tokenises a line according to BBDB format rules.

    In particular, respect ()."""

def parse_line(line):
    """Parse the provided line and return a nested dict of values"""
    # line = """["Jane" "Doe" nil nil (["Mobile" "+61 4123 456 789"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
    line = line.strip()
    if line.startswith(';'):
        return
    if not line.startswith('['):
        raise ValueError("Doesn't start with a '['!")
    if not line.endswith(']'):
        raise ValueError("Doesn't end with a ']'!")

    result = {}

    line = line[1:-1]
    tokens = shlex.split(line)

    result['firstname'] = tokens.pop(0)
    result['lastname'] = tokens.pop(0)
    _ = tokens.pop(0)
    result['company'] = tokens.pop(0)
    if result['company'] == 'nil':
        result['company'] = None

    if tokens[0] == 'nil':
        result['phone'] = {}
    else:
        if not tokens[0].startswith('(['):
            raise ValueError("Misformed phone block")

        phones = tokens[:next(index for index, item in enumerate(tokens) if item.endswith('])')) + 1]
        phones[0] = phones[0][1:]
        phones[-1] = phones[-1][:-1]
        tokens = tokens[len(phones):]
        it = iter(phones)
        result['phone'] = {}
        for key, value in zip(*[it] * 2):
            key = key.lstrip('[')
            value = value.rstrip(']')
            print key, value
            result['phone'][key] = value
            print "phones", phones

    print "leftover", tokens

    return result
