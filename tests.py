import unittest


class SimpleTest(unittest.TestCase):
    """Jarvy test cases."""

    def test_starting_out(self):
        self.assertEqual(1, 1)

    def setUp(self):
        import jarvy

    def tearDown(self):
        pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()
