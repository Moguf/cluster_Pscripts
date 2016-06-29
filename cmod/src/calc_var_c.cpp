#include "Python.h"
#include "calc_var_c.h"
#include <math.h>

static PyObject *calcVarError;

double euclidean(double xyz1[3],double xyz2[3]){
    return sqrt(pow(xyz1[0]-xyz2[0],2)+pow(xyz1[1]-xyz2[1],2)+pow(xyz1[2]-xyz2[2],2));
}

PyObject *calc(PyObject *xyzlist,PyObject *ninfolist)
{
    int xlen = PyList_Size(xyzlist);
    int nlen = PyList_Size(ninfolist);
    int natoms = PyList_Size(PyList_GetItem(xyzlist,0));
    double xyz1[3],xyz2[3],tmp;
    PyObject *frame,*pxyz1,*pxyz2,*ncon,*py_result,*row;
    long icon,jcon;
    double c_result[xlen][nlen];


    py_result = PyList_New(nlen);


    for(int i=0;i<xlen;i++){
        frame = PyList_GetItem(xyzlist,i);

        for(int j=0;j<nlen;j++){
            ncon = PyList_GetItem(ninfolist,j);
            icon = PyInt_AsLong(PyList_GetItem(ncon,0));
            jcon = PyInt_AsLong(PyList_GetItem(ncon,1));
            pxyz1 = PyList_GetItem(frame,icon);
            pxyz2 = PyList_GetItem(frame,jcon);

            for(int k=0;k<3;k++){
                xyz1[k] = PyFloat_AsDouble(PyList_GetItem(pxyz1,k));
                xyz2[k] = PyFloat_AsDouble(PyList_GetItem(pxyz2,k));
            }
            c_result[i][j] = euclidean(xyz1,xyz2);
        }

    }

    for(int i=0;i<nlen;i++){
        row = PyList_New(xlen);
        for(int j=0;j<xlen;j++){
            PyList_SetItem(row,j,PyFloat_FromDouble(c_result[j][i]));
        }
        PyList_SetItem(py_result,i,row);
    }

    return py_result;
}
    

static PyObject *
wrap_calc_var_c(PyObject *self,PyObject *args)
{
    PyObject *xyzlist,*ninfolist;

    if(!PyArg_ParseTuple(args,"OO", &xyzlist,&ninfolist))
        return NULL;
    
    return calc(xyzlist,ninfolist);
}


static PyMethodDef calcVarMethods[] = {
    {"calc",wrap_calc_var_c,METH_VARARGS,"Caluclating variances from trajctory."},
    {NULL,NULL,0,NULL}
};

PyMODINIT_FUNC
initcalcVarC(void)
{
    PyObject *m;
    m = Py_InitModule("calcVarC",calcVarMethods);
    if(m == NULL)
        return;
    calcVarError = PyErr_NewException("calcVar.error",NULL,NULL);
    Py_INCREF(calcVarError);
    PyModule_AddObject(m,"error",calcVarError);
}

    
