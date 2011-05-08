import shlex

def tokenise(line):
    """Tokenises a line according to BBDB format rules.

    In particular, respect ()."""

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

    temp = []
    in_pair = False
    it = iter(raw_tokens)
    for token in it:
        if token.startswith('(') and token.endswith(')'):
            tokens.append([token[1:-1]])
        elif token.startswith('('):
            if token[1] == '[':
                next_token = next(it)
                temp.append([token[2:], next_token[:-1]])
            else:
                temp.append(token[1:])
        elif token.endswith(')'):
            if temp:
                temp.append(token[:-1])
                tokens.append(temp)
                temp = []
        else:
            if temp:
                t = temp
            else:
                t = tokens
            if token[0] == '[':
                next_token = next(it)
                t.append([token[1:], next_token[:-1]])
            else:
                t.append(token)

    print line
    print raw_tokens
    print tokens
    return tokens

def parse_line(line):
    """Parse the provided line and return a nested dict of values"""
    # firstname lastname aliases company phone something email metadata notes
    # line = """["Jane" "Doe" nil nil (["Mobile" "+61 4123 456 789"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""

    result = {}

    line = line[1:-1]
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
            print key, value
            result['phone'][key] = value
            print "phones", phones

    print "leftover", tokens

    return result
