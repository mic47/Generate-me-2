#!/bin/bash
#
time pypy findFeatures.py data/zoznam lala features_definition 500 50 #
time pypy extractFeatures.py features_definition lala features.csv #
(head -n 1 features.csv ; tac features.csv | head -n -1 |shuf ) > features_shuffled.csv #
