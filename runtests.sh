#!/usr/bin/env bash

# remove exisiting output test files
rm -rf tests/interpreter/test_files/output/*

# run tests
pytest

# Double check if all files match
cmp --silent tests/interpreter/test_files/expected/output_1.txt tests/interpreter/test_files/output/output_1.txt && echo '### SUCCESS: Files Are Identical! o1 ###' || echo '### WARNING: Files Are Different! o1 ###'
cmp --silent tests/interpreter/test_files/expected/output_2.txt tests/interpreter/test_files/output/output_2.txt && echo '### SUCCESS: Files Are Identical! o2 ###' || echo '### WARNING: Files Are Different! o2 ###'
cmp --silent tests/interpreter/test_files/expected/output_3.txt tests/interpreter/test_files/output/output_3.txt && echo '### SUCCESS: Files Are Identical! o3 ###' || echo '### WARNING: Files Are Different! o3 ###'
cmp --silent tests/interpreter/test_files/expected/output_4.txt tests/interpreter/test_files/output/output_4.txt && echo '### SUCCESS: Files Are Identical! o4 ###' || echo '### WARNING: Files Are Different! o4 ###'
cmp --silent tests/interpreter/test_files/expected/output_5.txt tests/interpreter/test_files/output/output_5.txt && echo '### SUCCESS: Files Are Identical! o5 ###' || echo '### WARNING: Files Are Different! o5 ###'
cmp --silent tests/interpreter/test_files/expected/output_6.txt tests/interpreter/test_files/output/output_6.txt && echo '### SUCCESS: Files Are Identical! o6 ###' || echo '### WARNING: Files Are Different! o6 ###'
cmp --silent tests/interpreter/test_files/expected/output_7.txt tests/interpreter/test_files/output/output_7.txt && echo '### SUCCESS: Files Are Identical! o7 ###' || echo '### WARNING: Files Are Different! o7 ###'
cmp --silent tests/interpreter/test_files/expected/output_8.txt tests/interpreter/test_files/output/output_8.txt && echo '### SUCCESS: Files Are Identical! o8 ###' || echo '### WARNING: Files Are Different! o8 ###'
cmp --silent tests/interpreter/test_files/expected/output_9.txt tests/interpreter/test_files/output/output_9.txt && echo '### SUCCESS: Files Are Identical! o9 ###' || echo '### WARNING: Files Are Different! o9 ###'
cmp --silent tests/interpreter/test_files/expected/output_10.txt tests/interpreter/test_files/output/output_10.txt && echo '### SUCCESS: Files Are Identical! o10 ###' || echo '### WARNING: Files Are Different! o10 ###'
cmp --silent tests/interpreter/test_files/expected/output_11.txt tests/interpreter/test_files/output/output_11.txt && echo '### SUCCESS: Files Are Identical! o11 ###' || echo '### WARNING: Files Are Different! o11 ###'
cmp --silent tests/interpreter/test_files/expected/output_12.txt tests/interpreter/test_files/output/output_12.txt && echo '### SUCCESS: Files Are Identical! o12 ###' || echo '### WARNING: Files Are Different! o12 ###'
cmp --silent tests/interpreter/test_files/expected/output_13.txt tests/interpreter/test_files/output/output_13.txt && echo '### SUCCESS: Files Are Identical! o13 ###' || echo '### WARNING: Files Are Different! o13 ###'
cmp --silent tests/interpreter/test_files/expected/output_14.txt tests/interpreter/test_files/output/output_14.txt && echo '### SUCCESS: Files Are Identical! o14 ###' || echo '### WARNING: Files Are Different! o14 ###'
cmp --silent tests/interpreter/test_files/expected/output_15.txt tests/interpreter/test_files/output/output_15.txt && echo '### SUCCESS: Files Are Identical! o15 ###' || echo '### WARNING: Files Are Different! o15 ###'
cmp --silent tests/interpreter/test_files/expected/output_16.txt tests/interpreter/test_files/output/output_16.txt && echo '### SUCCESS: Files Are Identical! o16 ###' || echo '### WARNING: Files Are Different! o16 ###'
cmp --silent tests/interpreter/test_files/expected/output_17.txt tests/interpreter/test_files/output/output_17.txt && echo '### SUCCESS: Files Are Identical! o17 ###' || echo '### WARNING: Files Are Different! o17 ###'
cmp --silent tests/interpreter/test_files/expected/output_18.txt tests/interpreter/test_files/output/output_18.txt && echo '### SUCCESS: Files Are Identical! o18 ###' || echo '### WARNING: Files Are Different! o18 ###'
cmp --silent tests/interpreter/test_files/expected/output_19.txt tests/interpreter/test_files/output/output_19.txt && echo '### SUCCESS: Files Are Identical! o19 ###' || echo '### WARNING: Files Are Different! o19 ###'
cmp --silent tests/interpreter/test_files/expected/output_20.txt tests/interpreter/test_files/output/output_20.txt && echo '### SUCCESS: Files Are Identical! o20 ###' || echo '### WARNING: Files Are Different! o20 ###'
cmp --silent tests/interpreter/test_files/expected/output_21.txt tests/interpreter/test_files/output/output_21.txt && echo '### SUCCESS: Files Are Identical! o21 ###' || echo '### WARNING: Files Are Different! o21 ###'

echo '[note]: Interpreter test files located in: "tests/interpreter/test_files/"'
