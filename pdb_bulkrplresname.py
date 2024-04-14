#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 João Pedro Rodrigues
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright 2024 Vladimir O. Talibov 
# Modifications, based on pdb_rplresname:
# - first input argument is changed; takes one 1-3 char resname
# - all resnames in the pdb file will be changed to the specified resname.
# - author and email are removed from the module docstring.

"""
Performs replacement of all residue names by a single specified name.

For selective replacement of a particular name by another, use
pdb_rplresname from pdb-tools.

Usage:
    python pdb_bulkrplresname.py -<to> <pdb file>

Example:
    python pdb_bulkrplresname.py -INH macrocycle.pdb # changes all residues to INH

This program is modified pdb_rplresname from `pdb-tools` suite of utilities, see:
https://github.com/haddocking/pdb-tools
"""

import os
import sys

__author__ = ["Joao Rodrigues", "Joao M.C. Teixeira"]
__email__ = ["j.p.g.l.m.rodrigues@gmail.com", "joaomcteixeira@gmail.com"]


def check_input(args):
    """Checks whether to read from stdin/file and validates user input/options.
    """

    # Defaults
    option = ''
    fh = sys.stdin  # file handle

    if len(args) == 1:
        # option & Pipe
        if args[0].startswith('-'):
            option = args[0][1:]
            if sys.stdin.isatty():  # ensure the PDB data is streamed in
                emsg = 'ERROR!! No data to process!\n'
                sys.stderr.write(emsg)
                sys.stderr.write(__doc__)
                sys.exit(1)
        else:
            emsg = 'ERROR!! Option not valid: \'{}\'\n'
            sys.stderr.write(emsg.format(args[0]))
            sys.stderr.write(__doc__)
            sys.exit(1)

    elif len(args) == 2:
        # Two options: option & File
        if not args[0].startswith('-'):
            emsg = 'ERROR! First argument is not an option: \'{}\'\n'
            sys.stderr.write(emsg.format(args[0]))
            sys.stderr.write(__doc__)
            sys.exit(1)

        if not os.path.isfile(args[1]):
            emsg = 'ERROR!! File not found or not readable: \'{}\'\n'
            sys.stderr.write(emsg.format(args[1]))
            sys.stderr.write(__doc__)
            sys.exit(1)

        option = args[0][1:]
        fh = open(args[1], 'r')

    else:  # Whatever ...
        sys.stderr.write(__doc__)
        sys.exit(1)

    name_to = option

    if not (1 <= len(name_to) <= 3):
        emsg = 'ERROR!! Residue names must have one to three characters: \'{}\''
        sys.stderr.write(emsg.format(name_to))
        sys.exit(1)

    return (fh, name_to)


def run(fhandle, name_to):
    """
    Change the residue name of residues matching a pattern to another.

    This function is a generator.

    Parameters
    ----------
    fhandle : a line-by-line iterator of the original PDB file.

    name_from : str
        The original name of the residue to change.

    name_to : str
        The name to change to.

    Yields
    ------
    str (line-by-line)
        The modified (or not) PDB line.
    """

    records = ('ATOM', 'HETATM', 'TER', 'ANISOU')
    for line in fhandle:
        if line.startswith(records):
            yield line[:17] + name_to.rjust(3) + line[20:]
            continue
        yield line


rename_residues = run


def main():
    # Check Input
    pdbfh, name_to = check_input(sys.argv[1:])

    # Do the job
    new_pdb = run(pdbfh, name_to)

    # Output results
    try:
        _buffer = []
        _buffer_size = 5000  # write N lines at a time
        for lineno, line in enumerate(new_pdb):
            if not (lineno % _buffer_size):
                sys.stdout.write(''.join(_buffer))
                _buffer = []
            _buffer.append(line)

        sys.stdout.write(''.join(_buffer))
        sys.stdout.flush()
    except IOError:
        # This is here to catch Broken Pipes
        # for example to use 'head' or 'tail' without
        # the error message showing up
        pass

    # last line of the script
    # Close file handle even if it is sys.stdin, no problem here.
    pdbfh.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
