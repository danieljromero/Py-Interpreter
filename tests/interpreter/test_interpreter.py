import os
import filecmp
import pytest

from interpreter import interpreter as py



class TestInterpreter:
    def test_extract_wrong_file(self):
        with pytest.raises(TypeError):
            py.extract('file.csv')

    def test_input_1(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_1.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_1.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_1.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_2(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_2.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_2.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_2.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_3(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_3.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_3.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_3.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_4(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_4.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_4.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_4.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_5(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_5.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_5.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_5.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_6(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_6.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_6.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_6.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_7(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_7.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_7.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_7.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_8(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_8.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_8.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_8.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_9(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_9.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_9.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_9.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_10(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_10.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_10.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_10.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_11(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_11.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_11.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_11.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_12(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_12.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_12.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_12.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_13(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_13.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_13.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_13.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_14(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_14.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_14.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_14.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_15(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_15.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_15.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_15.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_16(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_16.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_16.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_16.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_17(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_17.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_17.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_17.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_18(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_18.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_18.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_18.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_19(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_19.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_19.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_19.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_20(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_20.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_20.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_20.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True

    def test_input_21(self):
        input = os.path.join(os.getcwd(), 'tests/interpreter/test_files/input/input_21.txt')
        output = os.path.join(os.getcwd(), 'tests/interpreter/test_files/output/output_21.txt')
        expected = os.path.join(os.getcwd(), 'tests/interpreter/test_files/expected/output_21.txt')
        py.interpreter(input, output)
        assert filecmp.cmp(expected, output) == True
