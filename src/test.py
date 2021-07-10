import unittest
from client import Client


class TestAthleteMethods(unittest.TestCase):
    def test_get_athlete(self):
        TT_ID = 116682
        tom = Client().get_athlete(TT_ID)
        self.assertEqual(tom.id, TT_ID)
        self.assertEqual(tom.nation, "England")
        self.assertEqual(tom.name, "Thomas Taylor")

        print(tom.id)
        print(tom.name)
        print(tom.nation)

        best_results = Client().get_all_results(TT_ID)

        print()


test = TestAthleteMethods()
test.test_get_athlete()
