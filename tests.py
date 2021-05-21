from django.test import TestCase

class pytest_tests(TestCase):

    # Create your tests here.
    def test_always_passes(self):
        assert True

    def test_always_fails(self):
        assert False

    def test_uppercase(self):
        assert "loud noises".upper() == "LOUD NOISES"

    def test_reversed(self):
        assert list(reversed([1, 2, 3, 4])) == [4, 3, 2, 1]

    def test_some_primes(self):
        assert 37 in {
            num
            for num in range(1, 50)
            if num != 1 and not any([num % div == 0 for div in range(2, num)])
        }

