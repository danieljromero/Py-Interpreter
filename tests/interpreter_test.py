import subprocess

from interpreter import interpreter as py

py.interpreter("text/input/input_1.txt", "text/result/pytest1.txt")
py.interpreter("text/input/input_2.txt", "text/result/pytest2.txt")
py.interpreter("text/input/input_3.txt", "text/result/pytest3.txt")
py.interpreter("text/input/input_4.txt", "text/result/pytest4.txt")
py.interpreter("text/input/input_5.txt", "text/result/pytest5.txt")
py.interpreter("text/input/input_6.txt", "text/result/pytest6.txt")
py.interpreter("text/input/input_7.txt", "text/result/pytest7.txt")
py.interpreter("text/input/input_8.txt", "text/result/pytest8.txt")
py.interpreter("text/input/input_9.txt", "text/result/pytest9.txt")
py.interpreter("text/input/input_10.txt", "text/result/pytest10.txt")
py.interpreter("text/input/input_11.txt", "text/result/pytest11.txt")
py.interpreter("text/input/input_12.txt", "text/result/pytest12.txt")
py.interpreter("text/input/input_13.txt", "text/result/pytest13.txt")
py.interpreter("text/input/input_14.txt", "text/result/pytest14.txt")
py.interpreter("text/input/input_15.txt", "text/result/pytest15.txt")
py.interpreter("text/input/input_16.txt", "text/result/pytest16.txt")
py.interpreter("text/input/input_17.txt", "text/result/pytest17.txt")
py.interpreter("text/input/input_18.txt", "text/result/pytest18.txt")
py.interpreter("text/input/input_19.txt", "text/result/pytest19.txt")
py.interpreter("text/input/input_20.txt", "text/result/pytest20.txt")
py.interpreter("text/input/input_21.txt", "text/result/pytest21.txt")

subprocess.call("./pycheck.sh", shell=True)  # Calls shell script
