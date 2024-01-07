from collections import defaultdict

import pandas as pd

from .specification import SPECIFICATION
from .bonds import guess_bonds as guess_bonds_func


def parse_line(line, mdl_idx=0):
    """
    slice a string in specific spots (must include edges,
    left inclusive and right exclusive) and return appropriate types
    """
    line = line.strip()

    for record_type, spec in SPECIFICATION.items():
        if line.startswith(record_type):
            items = []
            for rng, dtype, colname in spec:
                if colname == 'model_id':
                    # special case for coordinates, add the model id
                    items.append(mdl_idx)
                else:
                    # split the line based on the specs
                    field = line[rng[0]:rng[1]]
                    try:
                        field = dtype(field.strip()) or None
                    except ValueError:
                        field = None
                    items.append(field)
            return record_type, items
    return None, None


def read_pdb(path, guess_bonds=True):
    with open(path, 'r') as f:
        lines = f.readlines()

    records = defaultdict(list)
    mdl_idx = 0
    # parse contents
    for line in lines:
        record_type, fields = parse_line(line, mdl_idx)
        if record_type == 'MODEL':
            mdl_idx = fields[0]
        elif record_type == 'ENDMDL':
            mdl_idx += 1
        elif record_type is not None:
            records[record_type].append(fields)

    # put in dataframes with appropriate column names
    data = {}
    for record_type, fields in records.items():
        _, _, columns = zip(*SPECIFICATION[record_type])
        df = pd.DataFrame(fields, columns=columns)
        data[record_type] = df

    # merge ATOM and HETATM for ease of processing
    atoms = []
    for atm_type in ('ATOM', 'HETATM'):
        try:
            some_atoms = data.pop(atm_type)
        except KeyError:
            continue
        some_atoms['type'] = atm_type
        atoms.append(some_atoms)
    if len(atoms) > 0:
        data['ATOMS'] = pd.concat(atoms, ignore_index=True)

    # clean up CONECT so it's 1 to 1 column
    if 'CONECT' in data:
        # melt df and drop variable names (every column is equivalent except atom1)
        conect = data['CONECT'].melt('atom1', value_name='atom2').drop('variable', 1)
        conect = conect.dropna().astype(int)
        data['CONECT'] = conect

    if guess_bonds:
        bonds = guess_bonds_func(data['ATOMS'])
        if bonds.size > 0:
            data[f'BONDS_GUESSED'] = pd.DataFrame(bonds, columns=['atom1', 'atom2'])

    return dict(data)
