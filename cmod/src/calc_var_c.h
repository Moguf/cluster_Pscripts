#ifndef _calcvarc
#define _calcvarc

double euclidean(double xyz1[3],double xyz2[3]);
PyObject *calc(PyObject *xyzlist,PyObject *ninfolist);
static PyObject *wrap_calc_var_c(PyObject *self,PyObject *args);
PyMODINIT_FUNC initcalcVarC(void);

#endif
