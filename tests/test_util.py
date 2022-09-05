from haystackparser.util import populateListWithNone


class Test_populateListWithNone:
    def test_populate_Empty(self):
        assert populateListWithNone([], 8) == [None, None, None, None,
                                               None, None, None, None]

    def test_populate_NotEmpty(self):
        assert populateListWithNone(["test", 'test'], 8) == ["test", 'test', None, None,
                                                             None, None, None, None]
