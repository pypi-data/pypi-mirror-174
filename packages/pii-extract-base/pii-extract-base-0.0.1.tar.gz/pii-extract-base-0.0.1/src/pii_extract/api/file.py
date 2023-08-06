"""
File-based API
"""

import sys

from typing import Dict, List, TextIO

from pii_data.types.localdoc import LocalSrcDocumentFile
from pii_data.helper.io import openfile
from pii_data.helper.exception import InvArgException

from ..helper.types import TYPE_STR_LIST
from . import PiiProcessor


def print_tasks(lang: str, proc: PiiProcessor, out: TextIO):
    """
    Print out the list of built tasks
    """
    print(f". Built tasks [language={lang}]", file=out)
    for (pii, country), tasklist in proc.task_info().items():
        print(f"\n {pii.name}  [country={country}]   ", file=out)
        for name, doc in tasklist:
            print(f"     {name}: {doc}", file=out)


# ----------------------------------------------------------------------


def process_file(infile: str,
                 outfile: str,
                 load_plugins: bool = True,
                 taskfile: TYPE_STR_LIST = None,
                 lang: str = None,
                 country: List[str] = None,
                 tasks: List[str] = None,
                 chunk_context: bool = False,
                 outfmt: str = None,
                 debug: bool = False,
                 show_tasks: bool = False,
                 show_stats: bool = False) -> Dict:
    """
    Process a number of PII tasks on a file holding a source document
      :param infile: input source document
      :param outfile: output file where to store the detected PII entities
      :param load_plugins: load pii-extract task plugins
      :param taskfile: JSON task definition files to add to the set (in addition
         to the tasks collected via plugins)
      :param lang: language the document is in (if not defined inside the doc)
      :param country: countries to build tasks for (if None, all applicable
         countries for the language are used)
      :param tasks: specific set of PII tasks to build (default is all
         applicable tasks)
      :param chunk_context: when iterating the document, generate contexts
         for each chunk
      :param outfmt: format for the output list of tasks: "json" or "ndjson"

      :return: a dictionary with stats on the detection
    """
    # Load document and define the language
    doc = LocalSrcDocumentFile(infile)
    meta = doc.metadata
    lang = meta.get("main_lang") or meta.get("lang") or lang
    if not lang:
        raise InvArgException("no language defined in options or document")

    # Create the object
    proc = PiiProcessor(load_plugins=load_plugins, debug=debug)
    if taskfile:
        proc.add_json_tasks(taskfile)

    # Build the task objects
    proc.build_tasks(lang, country, tasks=tasks)
    if show_tasks:
        print_tasks(lang, proc, sys.stderr)

    if outfmt is None:
        if outfile.endswith('.json'):
            outfmt = 'json'
        elif outfile.endswith('.ndjson'):
            outfmt = 'ndjson'
        else:
            raise InvArgException("no output format specified")

    if debug:
        print(". Reading from:", infile, file=sys.stderr)
        print(". Writing to:", outfile, file=sys.stderr)

    # Process the file
    piic = proc(doc, chunk_context=chunk_context)

    # Dump results
    with openfile(outfile, "wt") as fout:
        piic.dump(fout, format=outfmt)

    stats = proc.get_stats()
    if show_stats:
        print("\n. Statistics:", file=sys.stderr)
        for k, v in stats.items():
            print(f"  {k:20} :  {v:5}", file=sys.stderr)

    return stats
