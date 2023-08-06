#if CYTHON_COMPILING_IN_CPYTHON || CYTHON_COMPILING_IN_LIMITED_API || CYTHON_USE_TYPE_SPECS
static int __Pyx_validate_bases_tuple(const char *type_name, Py_ssize_t dictoffset, PyObject *bases) {
    Py_ssize_t i, n = PyTuple_GET_SIZE(bases);
    for (i = 1; i < n; i++)
    {
        PyObject *b0 = PyTuple_GET_ITEM(bases, i);
        PyTypeObject *b;
#if PY_MAJOR_VERSION < 3
        if (PyClass_Check(b0))
        {
            PyErr_Format(PyExc_TypeError, "base class '%.200s' is an old-style class",
                         PyString_AS_STRING(((PyClassObject*)b0)->cl_name));
            return -1;
        }
#endif
        b = (PyTypeObject*) b0;
        if (!__Pyx_PyType_HasFeature(b, Py_TPFLAGS_HEAPTYPE))
        {
            __Pyx_TypeName b_name = __Pyx_PyType_GetName(b);
            PyErr_Format(PyExc_TypeError,
                "base class '" __Pyx_FMT_TYPENAME "' is not a heap type", b_name);
            __Pyx_DECREF_TypeName(b_name);
            return -1;
        }
        if (dictoffset == 0 && b->tp_dictoffset)
        {
            __Pyx_TypeName b_name = __Pyx_PyType_GetName(b);
            PyErr_Format(PyExc_TypeError,
                "extension type '%.200s' has no __dict__ slot, "
                "but base type '" __Pyx_FMT_TYPENAME "' has: "
                "either add 'cdef dict __dict__' to the extension type "
                "or add '__slots__ = [...]' to the base type",
                type_name, b_name);
            __Pyx_DECREF_TypeName(b_name);
            return -1;
        }
    }
    return 0;
}
#endif

