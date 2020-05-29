import png

from dtedifier.readers import (
    DTED,
)

elevation = DTED(open('../tests/fixtures/N59.DT2', 'rb').read()).data.elevation_trimmed()
png_data = []
maximum_height = 0

for row in elevation:
    maximum_height = max(maximum_height, max([x for x in row if x is not None]))

for row in elevation:
    row_data = []

    for point in row:
        if point is None:
            row_data.append(255)
            row_data.append(0)
            row_data.append(0)
        elif point < 0:
            row_data.append(0)
            row_data.append(255)
            row_data.append(0)
        elif point == 0:
            row_data.append(0)
            row_data.append(0)
            row_data.append(255)
        else:
            val = int(point / maximum_height * 255)
            row_data.append(val)
            row_data.append(val)
            row_data.append(val)

    png_data.append(row_data)

writer = png.Writer(len(elevation[0]), len(elevation), greyscale=False)
f = open('png.png', 'wb')
writer.write(f, png_data)
f.close()
