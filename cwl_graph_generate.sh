#!/bin/bash

CWL=$1
BASE=`basename $CWL .cwl`

echo "Converting $CWL -> $BASE.graph"
/opt/cwl_graph_generate.py $CWL $BASE.graph

echo "Generating $BASE.png"
dot -Tpng $BASE.graph > $BASE.png

