#!/bin/bash

CWL=$1
BASE=`basename $CWL .cwl`

/opt/cwl_graph_generate.py $CWL $BASE.graph
dot -Tpng $BASE.graph > $BASE.png

