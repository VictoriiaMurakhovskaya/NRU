import unittest
from memory import Memory


class TestMethods(unittest.TestCase):
    def test1(self):
        a = Memory(ph_cells=4)
        a.addprocess(2)
        a.addprocess(4)
        for i in range(0, 10):
            process, page = a.choosepagevm()
            self.assertGreaterEqual(page, 0)
            self.assertGreaterEqual(len(a.vm.processes[process].allocation) - 1, page)
            self.assertIn(process, [0, 1])
