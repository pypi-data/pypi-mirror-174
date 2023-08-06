#include <Python.h>

#include "solpos00.h"

static PyObject *
decode_error(long code, struct posdata *pdat)
{
    if (code & (1L << S_YEAR_ERROR)) {
        PyErr_Format(PyExc_ValueError,
                     "Please fix the year: %d (allowed range: [1950-2050])\n",
                     pdat->year);
        return NULL;
    }
    if (code & (1L << S_MONTH_ERROR)) {
        PyErr_Format(PyExc_ValueError,
                     "Please fix the month: %d (allowed range: [1-12])\n",
                     pdat->month);
        return NULL;
    }
    if (code & (1L << S_DAY_ERROR)) {
        PyErr_Format(
            PyExc_ValueError,
            "Please fix the day-of-month: %d (allowed range: [1-31])\n",
            pdat->day);
        return NULL;
    }
    if (code & (1L << S_DOY_ERROR)) {
        PyErr_Format(
            PyExc_ValueError,
            "Please fix the day-of-year: %d (allowed range: [1-366])\n",
            pdat->daynum);
        return NULL;
    }
    if (code & (1L << S_HOUR_ERROR)) {
        PyErr_Format(PyExc_ValueError,
                     "Please fix the hour: %d (allowed range: [0-24])\n",
                     pdat->hour);
        return NULL;
    }
    if (code & (1L << S_MINUTE_ERROR)) {
        PyErr_Format(PyExc_ValueError,
                     "Please fix the minute: %d (allowed range: [0-59])\n",
                     pdat->minute);
        return NULL;
    }
    if (code & (1L << S_SECOND_ERROR)) {
        PyErr_Format(PyExc_ValueError,
                     "Please fix the second: %d (allowed range: [0-59])\n",
                     pdat->second);
        return NULL;
    }
    if (code & (1L << S_TZONE_ERROR)) {
        PyErr_SetString(PyExc_ValueError,
                        "Please fix the time zone (allowed range: [-12-12])\n");
        return NULL;
    }
    if (code & (1L << S_INTRVL_ERROR)) {
        PyErr_Format(PyExc_ValueError,
                     "Please fix the interval: %d (allowed range: [0-28800])\n",
                     pdat->interval);
        return NULL;
    }
    if (code & (1L << S_LAT_ERROR)) {
        PyErr_SetString(PyExc_ValueError,
                        "Please fix the latitude (allowed range: [-90-90])\n");
        return NULL;
    }
    if (code & (1L << S_LON_ERROR)) {
        PyErr_SetString(
            PyExc_ValueError,
            "Please fix the longitude (allowed range: [-180-180])\n");
        return NULL;
    }
    if (code & (1L << S_TEMP_ERROR)) {
        PyErr_SetString(
            PyExc_ValueError,
            "Please fix the temperature (allowed range: [-100-100])\n");
        return NULL;
    }
    if (code & (1L << S_PRESS_ERROR)) {
        PyErr_SetString(PyExc_ValueError,
                        "Please fix the pressure (allowed range: [0-2000])\n");
        return NULL;
    }
    if (code & (1L << S_TILT_ERROR)) {
        PyErr_SetString(PyExc_ValueError,
                        "Please fix the tilt (allowed range: [-180-180])\n");
        return NULL;
    }
    if (code & (1L << S_ASPECT_ERROR)) {
        PyErr_SetString(PyExc_ValueError,
                        "Please fix the aspect (allowed range: [-360-360])\n");
        return NULL;
    }
    if (code & (1L << S_SBWID_ERROR)) {
        PyErr_SetString(
            PyExc_ValueError,
            "Please fix the shadowband width (allowed range: [1-100])\n");
        return NULL;
    }
    if (code & (1L << S_SBRAD_ERROR)) {
        PyErr_SetString(
            PyExc_ValueError,
            "Please fix the shadowband radius (allowed range: [1-100])\n");
        return NULL;
    }
    if (code & (1L << S_SBSKY_ERROR)) {
        PyErr_SetString(
            PyExc_ValueError,
            "Please fix the shadowband sky factor (allowed range: [-1-1])\n");
        return NULL;
    }

    PyErr_Format(PyExc_NotImplementedError,
                 "Did not find the cause of the exception. This is most likely "
                 "a bug: %ld",
                 code);
    return NULL;
}

static PyObject *
_solpos(PyObject *self, PyObject *args, PyObject *kwargs)
{
    float longitude, latitude, timezone, aspect, press, sbwid, sbrad, sbsky,
        solcon, temp, tilt;
    int year, month, day, hour, minute, second, interval;

    static char *kwlist[] = {
        "year",   "month",    "day",      "hour",     "minute",
        "second", "timezone", "interval", "latitude", "longitude",
        "aspect", "press",    "sbwid",    "sbrad",    "sbsky",
        "solcon", "temp",     "tilt",     NULL,
    };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiiiiififfffffffff", kwlist,
                                     &year, &month, &day, &hour, &minute,
                                     &second, &timezone, &interval, &latitude,
                                     &longitude, &aspect, &press, &sbwid,
                                     &sbrad, &sbsky, &solcon, &temp, &tilt))
        return NULL;

    struct posdata pd, *pdat;
    pdat = &pd;
    S_init(pdat);

    pdat->function = ~S_DOY;

    pdat->year = year;
    pdat->month = month;
    pdat->day = day;
    pdat->hour = hour;
    pdat->minute = minute;
    pdat->second = second;
    pdat->timezone = timezone;
    pdat->interval = interval;
    pdat->latitude = latitude;
    pdat->longitude = longitude;
    pdat->aspect = aspect;
    pdat->press = press;
    pdat->sbwid = sbwid;
    pdat->sbrad = sbrad;
    pdat->sbsky = sbsky;
    pdat->solcon = solcon;
    pdat->temp = temp;
    pdat->tilt = tilt;

    long retval = S_solpos(pdat);
    // something went wrong, get the error from SOLPOS and raise it
    if (retval != 0) {
        decode_error(retval, pdat);
        // return NULL to indicate python an error happened since PyObject can't
        // be NULL
        return NULL;
    }
    // clang-format off
    return Py_BuildValue(
        // date and time
        "{s:i,s:i,s:i,s:i,s:i,s:i,s:f,"
        // interval, lat and lon
        "s:i,s:f,s:f,"
        // input and output parameters (all floats!)
        "s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f,s:f}",
        // date and time
        "year", pdat->year,
        "month", pdat->month,
        "day", pdat->day,
        "hour", pdat->hour,
        "minute", pdat->minute,
        "second", pdat->second,
        "timezone", pdat->timezone,
        // interval, lat and lon
        "interval", pdat->interval,
        "latitude", pdat->latitude,
        "longitude", pdat->longitude,
        // input- and output parameters
        "amass", pdat->amass,
        "ampress", pdat->ampress,
        "aspect", pdat->aspect,
        "azim", pdat->azim,
        "cosinc", pdat->cosinc,
        "coszen", pdat->coszen,
        "dayang", pdat->dayang,
        "declin", pdat->declin,
        "eclong", pdat->eclong,
        "ecobli", pdat->ecobli,
        "ectime", pdat->ectime,
        "elevetr", pdat->elevetr,
        "elevref", pdat->elevref,
        "eqntim", pdat->eqntim,
        "erv", pdat->erv,
        "etr", pdat->etr,
        "etrn", pdat->etrn,
        "etrtilt", pdat->etrtilt,
        "gmst", pdat->gmst,
        "hrang", pdat->hrang,
        "julday", pdat->julday,
        "lmst", pdat->lmst,
        "mnanom", pdat->mnanom,
        "mnlong", pdat->mnlong,
        "rascen", pdat->rascen,
        "press", pdat->press,
        "prime", pdat->prime,
        "sbcf", pdat->sbcf,
        "sbwid", pdat->sbwid,
        "sbrad", pdat->sbrad,
        "sbsky", pdat->sbsky,
        "solcon", pdat->solcon,
        "ssha", pdat->ssha,
        "sretr", pdat->sretr,
        "ssetr", pdat->ssetr,
        "temp", pdat->temp,
        "tilt", pdat->tilt,
        "tst", pdat->tst,
        "tstfix", pdat->tstfix,
        "unprime", pdat->unprime,
        "utime", pdat->utime,
        "zenetr", pdat->zenetr,
        "zenref", pdat->zenref);
}
// clang-format on

static struct PyMethodDef methods[] = {
    {"_solpos", (PyCFunction)_solpos, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {PyModuleDef_HEAD_INIT, "_solpos", NULL, -1,
                                    methods};

PyMODINIT_FUNC
PyInit__solpos(void)
{
    return PyModule_Create(&module);
}
