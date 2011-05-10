import shlex
from datetime import date

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
    in_assoc = False
    was_in_assoc = False
    result = []
    while tokens:
        token = tokens.pop(0)
        if token == '.':
            in_assoc = True
        elif token in ('(', '['):
            tokens, _temp, was_in_assoc = _parse(tokens)
            if not isinstance(_temp, dict):
                result.append(d[token[0]](_temp))
            else:
                result.append(_temp)
        elif token in (')', ']'):
            if was_in_assoc:
                result = dict(result)
                was_in_assoc = False
            return tokens, result, in_assoc
        else:
            result.append(token)

    return tokens, result, in_assoc

def parse(tokens):
    return _parse(tokens)[1]

def parse_line(line):
    """Parse the provided line and return a nested dict of values"""
    # firstname lastname aliases company phone something email metadata notes
    # line = """["Jane" "Doe" nil nil (["Mobile" "+61 4123 456 789"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""

    result = {}

    it = parse(tokenise(line))

    result['firstname'] = it[0]
    result['lastname'] = it[1]
    _ = it[2]
    result['company'] = it[3]
    if result['company'] == 'nil':
        result['company'] = None
    result['phone'] = dict(it[4])
    _ = it[5]
    result['email'] = it[6][0]
    result['random'] = it[7]
    _ = it[8]

    # handle specials
    if 'creation-date' in result['random']:
        result['random']['creation-date'] = date(*[int(x) for x in result['random']['creation-date'].split('-')])

    return result
