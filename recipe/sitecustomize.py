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