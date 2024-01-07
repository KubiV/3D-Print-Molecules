# PDB reader
`pdbreader` is a simple python library for parsing PDB (Protein Data Bank) files. It uses pandas DataFrames as its main data structure.

## Installation

```
pip install pdbreader
```

## Usage

```python
import pdbreader

pdb = pdbreader.read_pdb(pdb_path)
```

The resulting `pdb` dictionary contains an entry for each record type (`ATOM`, `CONECT`, etc) in the form of pandas DataFrames.

### Bond guessing
By default (disable with `guess_bonds=False`), the reader will attempt to guess bonds based on VDW radii and atom distances. These bonds are added to the dict. Differently from the `CONECT` records (which refer to the atom `id` column), these bonds are calculated on a coordinate basis, so they refer to the index of the `ATOM` and `HETATM` dataframes.

Note that alternate locations are not handled correctly yet, and will be considered separate atoms for bonding purposes.
