# test file names - 
# test_*.py
# *_test.py

# Pytest requires the test function names to start with test*. 
# pytest                #run test cases, F represents a test failure and dot(.) represents a test success.
# pytest -v             #more verbosity
# pytest <filename> -v  #To execute the tests from a specific file

def test_addition():
    assert 2 + 3 == 5

# Pytest provides two ways to run the subset of the test suite:
# Select tests to run based on substring matching of test names.
# Select tests groups to run based on the markers applied.
# pytest -k <substring> -v    #run tests whose function names contain the given substring

# Pytest provides many inbuilt markers such as xfail, skip and parametrize. Apart from that, 
# users can create their own marker names. Markers are applied on the tests using the syntax given below −
# @pytest.mark.<markername>
# To use markers, we have to import pytest module in the test file. 
# We can define our own marker names to the tests and run the tests having those marker names.
# To run the marked tests, we can use the following syntax −
# pytest -m <markername> -v

import pytest

@pytest.mark.great
def test_greater_equal():
   num = 100
   assert num >= 100

# Fixtures are functions, which will run before each test function to which it is applied. 
# Fixtures are used to feed some data to the tests such as database connections, URLs to test and 
# some sort of input data. Therefore, instead of running the same code for every test, 
# we can attach fixture function to the tests and it will run and return the data to the 
# test before executing each test. A function is marked as a fixture by −
# @pytest.fixture 

import pytest
@pytest.fixture
def input_value():
   input = 39
   return input
def test_divisible_by_3(input_value):
   assert input_value % 3 == 0

# A fixture function defined inside a test file has a scope within the test file only. 
# We cannot use that fixture in another test file. To make a fixture available to multiple 
# test files, we have to define the fixture function in a file called conftest.py


# Parameterizing of a test is done to run the test against multiple sets of inputs.
# @pytest.mark.parametrize
import pytest
@pytest.mark.parametrize("num, output",[(1,11),(2,22),(3,35),(4,44)])
def test_multiplication_11(num, output):
   assert 11*num == output
# Here, the test function test_multiplication_11 is going to run four times.