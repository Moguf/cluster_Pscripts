#include <Python.h>

static PyObject* dot(PyObject* list1,PyObject* list2)
{
    long size1=PyList_Size(list1);
    long size2=PyList_Size(list2);
    double temp,out_sum=0;
    long i;
    
    if(size1!=size2){
        return NULL;
    }
    for(i=0;i<size1;i++){
        temp=PyFloat_AsDouble(PyList_GetItem(list1,i))*PyFloat_AsDouble(PyList_GetItem(list2,i));
        out_sum+=temp;
    }
    return PyFloat_FromDouble(out_sum);
}

static PyObject* wrap_dot(PyObject* self,PyObject* args)
{
    PyObject *list1,*list2;
    if(!PyArg_ParseTuple(args,"OO",
                         &list1,
                         &list2
                         )){
        return NULL;
    }
    return dot(list1,list2);
}

static PyMethodDef dotmethods[]={
    {"dot",wrap_dot,METH_VARARGS},
    {NULL},
};
void initdot(){
    (void)Py_InitModule("dot",dotmethods);
}
