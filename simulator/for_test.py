def reshape_and_slice_satellites(tle_path, num_columns=3, num_rows=4):
    """
    Reshape satellite names into an array and slice it into several 3x4 rectangles.

    :param tle_path: Path to the TLE file.
    :param num_columns: Number of columns in each rectangle (width).
    :param num_rows: Number of rows in each rectangle (height).
    :return: List of rectangles, each containing 12 satellite names.
    """
    with open(tle_path, 'r') as file:
        lines = file.readlines()

    # Extract satellite names
    satellite_names = [line.strip() for line in lines if line.startswith('V')]

    print(satellite_names)

    # Ensure we have the correct total number of satellites
    if len(satellite_names) != 480:
        raise ValueError("The number of satellites does not match the expected total of 480.")

    # # Reshape the list into an array with columns representing satellites in order
    # satellites_array = [satellite_names[i:i + 12] for i in range(0, len(satellite_names), 12)]

    # print(satellites_array)

    rectangles = []

    # # Slice the array into 3x4 rectangles
    rows_per_submatrix = 3
    cols_per_submatrix = 4
    for row in range(0, 12, rows_per_submatrix):
        for col in range(0, 40, cols_per_submatrix):
            rectangle = []
            for i in range(row):
                for j in range(col):
                    rectangle.append(satellite_names[i][j])
            rectangles.append(rectangle)

    return rectangles


tle_path="guowang_tle.txt"
rectangles = reshape_and_slice_satellites(tle_path)
print(len(rectangles))