import contextlib
import importlib


__author__ = "Gavin Huttley"
__copyright__ = "Copyright 2007-2022, The Cogent Project"
__credits__ = ["Gavin Huttley", "Nick Shahmaras"]
__license__ = "BSD-3"
__version__ = "2022.10.31a1"
__maintainer__ = "Gavin Huttley"
__email__ = "Gavin.Huttley@anu.edu.au"
__status__ = "Alpha"

__all__ = ["align", "composable", "dist", "evo", "io", "sample", "translate", "tree"]


def _doc_summary(doc):
    """return first para of docstring"""
    result = []
    for line in doc.splitlines():
        line = line.strip()
        if not line:
            break
        result.append(line)
    return " ".join(result)


def _get_app_attr(name, is_composable):
    """returns app details for display"""

    modname, name = name.rsplit(".", maxsplit=1)
    mod = importlib.import_module(modname)
    obj = getattr(mod, name)

    _types = {"_data_types": [], "_return_types": []}

    for tys in _types:
        types = getattr(obj, tys, None) or []
        types = [types] if type(types) == str else types
        _types[tys] = [{None: ""}.get(e, e) for e in types]

    return [
        mod.__name__,
        name,
        is_composable,
        _doc_summary(obj.__doc__ or ""),
        ", ".join(sorted(_types["_data_types"])),
        ", ".join(sorted(_types["_return_types"])),
    ]


def available_apps():
    """returns Table listing the available apps"""
    from cogent3.util.table import Table

    from .composable import __app_registry

    # registration of apps does not happen until their modules are imported
    for name in __all__:
        importlib.import_module(f"cogent3.app.{name}")

    rows = []
    for app, is_comp in __app_registry.items():
        with contextlib.suppress(AttributeError):
            # probably a local scope issue in testing!
            rows.append(_get_app_attr(app, is_comp))

    header = ["module", "name", "composable", "doc", "input type", "output type"]
    return Table(header=header, data=rows)
