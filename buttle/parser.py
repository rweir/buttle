import shlex

def tokenise(line):
    """Tokenises a line according to BBDB format rules.

    In particular, respect () and []."""

    tokens = []
    line = line.strip()
    if line.startswith(';'):
        return
    if not line.startswith('['):
        raise ValueError("Doesn't start with a '['!")
    if not line.endswith(']'):
        raise ValueError("Doesn't end with a ']'!")
    line = line[1:-1]
    raw_tokens = shlex.split(line)

    tokens = []
    while raw_tokens:
        token = raw_tokens.pop(0)
        if token[0] in ('(', '[') and len(token) > 1:
            raw_tokens.insert(0, token[1:])
            raw_tokens.insert(0, token[0])
        elif token[-1] in (')', ']') and len(token) > 1:
            raw_tokens.insert(0, token[-1])
            raw_tokens.insert(0, token[:-1])
        else:
            tokens.append(token)

    return tokens

d = {'(': list, '[': tuple}

def _parse(tokens):
    result = []
    while tokens:
        token = tokens.pop(0)
        if token in ('(', '['):
            tokens, _temp = _parse(tokens)
            result.append(d[token[0]](_temp))
        elif token in (')', ']'):
            continue
        else:
            result.append(token)

    return tokens, result

def parse(tokens):
    return _parse(tokens)[1]

def parse_line(line):
    """Parse the provided line and return a nested dict of values"""
    # firstname lastname aliases company phone something email metadata notes
    # line = """["Jane" "Doe" nil nil (["Mobile" "+61 4123 456 789"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""

    result = {}

    tokens = tokenise(line)

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
            result['phone'][key] = value

    print "leftover", tokens

    return result
