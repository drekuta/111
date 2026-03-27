"""
Custom Django hook used to avoid a crash in the stock hook on some Windows/Python
setups where module file lookup may unexpectedly return None.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata


def _safe_collect_submodules(module_name: str):
    try:
        return collect_submodules(module_name)
    except Exception:
        return []


def _safe_collect_data_files(module_name: str):
    try:
        return collect_data_files(module_name, include_py_files=True)
    except Exception:
        return []


hiddenimports = _safe_collect_submodules("django")
datas = _safe_collect_data_files("django") + copy_metadata("django")

for module_name in (
    "config",
    "apps.core",
    "apps.forms_registry",
    "apps.templates_engine",
    "apps.docgen",
    "rest_framework",
):
    hiddenimports += _safe_collect_submodules(module_name)
    datas += _safe_collect_data_files(module_name)
