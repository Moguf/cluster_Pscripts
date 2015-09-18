#include <Python.h>

static PyObject* myadd(PyObject* num)
{
    long myaddnum=PyInt_AsLong(num);
    myaddnum++;
    return PyInt_FromLong(myaddnum);
}


static PyObject *
wrap_myadd(PyObject *self,PyObject *args)
{
    PyObject *innum;
 
   
    if(!PyArg_ParseTuple(args,"O"
                         ,&innum)){
        return NULL;
    }

    return myadd(innum);
}

static PyMethodDef myaddmethods[]={
    {"myadd",wrap_myadd,METH_VARARGS},
    {NULL},
};

void initmyadd(void){
    (void) Py_InitModule("myadd",myaddmethods);
}

