import unittest

import router

class TestRangeGeneration(unittest.TestCase):
    def testWithZeroRange(self):
        sRange = router.stepGen(0, 0)
        self.assertEqual(sRange, 0)
        self.assertEqual(router.stepRange(0, 0), [])

    def testWithSwappedMagnitudes(self):
        base, available = 10, 20
        sRange = router.stepGen(base, available)
        self.assertEqual(sRange, 0)

        # However given 10 as the base and 20 objects to service, we can only use the min
        seq = router.stepRange(base, available)
        self.assertEqual(len(seq), base)
        self.assertEqual(seq, [i for i in range(base)])

    def testWithInvaliInputs(self):
        self.assertEqual(router.stepGen(10, '20'), None)
        self.assertEqual(router.stepGen(None, 20), None)
        self.assertEqual(router.stepGen('10', 2), None)
        self.assertEqual(router.stepGen(-20, 2), None)
        self.assertEqual(router.stepGen(20, dict()), None)
        self.assertEqual(router.stepRange('10', 20), None)

    def testProperInputBaseLtAvail(self):
        base, avail = 2, 6
        seq = router.stepRange(base, avail)
        self.assertEqual(len(seq), base) # Could use: self.assertEqual(len(seq), min(base, avail))

        # In this case since base < avail expecting (base - 1) as the last item
        self.assertEqual(seq[-1], base-1)

    def testProperInputBaseGtAvail(self):
        base, avail = 10, 4
        seq = router.stepRange(base, avail)
        self.assertEqual(len(seq), avail)
        step = router.stepGen(base, avail)
        # Since base > avail expecting (base - step) as the last item
        self.assertEqual(seq[-1], base-step)

    def testProperInputBaseEqAvail(self):
        base, avail = 4, 4
        seq = router.stepRange(base, avail)
        self.assertEqual(len(seq), avail)
        step = router.stepGen(base, avail)
        # Since base == avail expecting (base - step) as the last item
        self.assertEqual(seq[-1], base-step)

class TestrangeSearch(unittest.TestCase):
    def setUp(self):
        self.content = [2, 3, 8, 10, 12, 13, 67]

    def testSearchingForAvailable(self):
        q = router.rangeSearch(self.content, 2)
        self.assertEqual(len(q), 2) # Expecting (low, high)
        self.assertEqual((0, 0,), q)

    def testRangeForItemsOutOfScope(self):
        q = router.rangeSearch(self.content, 9)
        self.assertEqual(len(q), 2)
        self.assertEqual((2, 3,), q) # 9 is between 8 and 10 which are (2, 3) in index terms

    def testRangeItemsOutOfEndElemRange(self):
        q = router.rangeSearch(self.content, 8710)
        self.assertEqual(len(q), 2)
        self.assertEqual((6, None,), q) # Known low elem 67 at index 6, Unknown high

        q1 = router.rangeSearch(self.content, 1)
        self.assertEqual(len(q1), 2)
        self.assertEqual((None, 0,), q1) # Known high elem 2 at index 0, Unknown low

class TestIndexAcquisition(unittest.TestCase):
    def setUp(self):
        self.base = 20 
        self.avail = 6
        self.seqRange = router.stepRange(self.base, self.avail)

    def testRangeValues(self): 
        expected = [3, 6, 9, 12, 15, 18]
        self.assertEqual(expected, self.seqRange)
        self.assertEqual(2, router.acquireIndex(self.seqRange, 11))
        self.assertEqual(0, router.acquireIndex(self.seqRange, -1))
        self.assertEqual(3, router.acquireIndex(self.seqRange, 12))
        self.assertEqual(5, router.acquireIndex(self.seqRange, 20))
        self.assertEqual(2, router.acquireIndex(self.seqRange, 10))
