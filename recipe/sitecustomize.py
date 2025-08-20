# Pathlib2’s test suite relies on internal test.support helpers (e.g., TESTFN, can_symlink, import_module) 
# that were moved to test.support.os_helper and test.support.import_helper in Python ≥3.11. 
# To keep the upstream tests working without patching them, we add a sitecustomize.py during the test phase. 
# This shim re-exports the missing helpers back into test.support so the tests pass on modern Python, 
# but it is not included in the built package.

# Shim for Python 3.11+ — restore atributes in test.support,
# which expect old tests pathlib2.

try:
    from test import support as _s
    # os_helper (Py3.11+): TESTFN, can_symlink, skip_unless_symlink, rmtree, EnvironmentVarGuard
    try:
        from test.support import os_helper as _oh  # Py3.11+
    except Exception:
        _oh = None
    # import_helper (Py3.11+): import_module
    try:
        from test.support import import_helper as _ih  # Py3.11+
    except Exception:
        _ih = None

    if _oh is not None:
        for _name in ("TESTFN", "can_symlink", "skip_unless_symlink",
                      "rmtree", "EnvironmentVarGuard"):
            if hasattr(_oh, _name) and not hasattr(_s, _name):
                setattr(_s, _name, getattr(_oh, _name))

    if _ih is not None:
        if not hasattr(_s, "import_module") and hasattr(_ih, "import_module"):
            _s.import_module = _ih.import_module
except Exception:
    pass