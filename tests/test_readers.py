from dtedifier.readers import (
    DTED
)

from test_descriptions import (
    example_accuracy_description,
    example_header,
    example_data_set,
)


def test_dted_reader(example_header, example_data_set, example_accuracy_description):
    dted = DTED(open('fixtures/N59.DT2', 'rb').read())

    assert dted.header == example_header
    assert dted.data_set_description == example_data_set
    assert dted.accuracy_description == example_accuracy_description
