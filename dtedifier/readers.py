from dtedifier.descriptions import (
    Header,
    DataSetDescription,
    AccuracyDescription,
    DataRecord,
)


class DTED:
    def __init__(self, b):
        self.header = Header.from_bytes(b[:80])
        self.data_set_description = DataSetDescription.from_bytes(b[80:728])
        self.accuracy_description = AccuracyDescription.from_bytes(b[728:3428])
        self.data = DataRecord.from_bytes(b[3428:], data_set_description=self.data_set_description)

        pass
