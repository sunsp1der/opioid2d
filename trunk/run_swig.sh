#!/bin/sh
swig -python -c++ -module cOpioid2D -o swig_dist/opioid2d_wrap.cxx -outdir swig_dist swig/opioid2d.i
cp swig_dist/cOpioid2D.py pyimpl/cOpioid2D.py