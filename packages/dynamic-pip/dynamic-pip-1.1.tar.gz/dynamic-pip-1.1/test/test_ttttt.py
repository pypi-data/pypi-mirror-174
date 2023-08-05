def long_description_load(filename):
    """
    long description loader
    """
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            _long_description = f.read()
    except FileNotFoundError:
        _long_description = ''

    RAW_LOGO = 'assets/logo.jpg'
    PYPI_LOGO = 'https://raw.githubusercontent.com/uguisu/dynamic-pip/main/assets/logo.jpg'
    RAW_MERMAID = '```mermaid'
    PYPI_MERMAID = '![mermaid](https://raw.githubusercontent.com/uguisu/dynamic-pip/main/assets/dependence_tree.jpg)'

    # remove logo
    _long_description = _long_description.replace(RAW_LOGO, PYPI_LOGO)

    rtn = []
    is_mermaid_area = False
    for ln in _long_description.splitlines(keepends=False):

        if is_mermaid_area:
            if ln == '```':
                # rollback flag
                is_mermaid_area = False
                # use an image instead
                rtn.append(PYPI_MERMAID)
            continue

        if (not is_mermaid_area) and (RAW_MERMAID == ln):
            # find mermaid area
            is_mermaid_area = True
            continue

        rtn.append(ln)

    return '\n'.join(rtn)



con = long_description_load('../README.md')


print(con)