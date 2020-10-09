#!/bin/bash

set -e

MODEL=models/petclinic_full.json
GEN_STOP_COND="random(vertex_coverage(100))"
TESTS_DIR=tests
altwalker check -m $MODEL "$GEN_STOP_COND"
altwalker verify -m $MODEL $TESTS_DIR
altwalker online tests -m $MODEL "$GEN_STOP_COND"

