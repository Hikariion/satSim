satellite_groups = {}
# 示例分组
# satellite_groups = {
#     'Satellite1': 'Group1',
#     'Satellite2': 'Group1',
#     'Satellite3': 'Group2',
#     # ... 其他卫星和它们的分组
# }

# grouped by orbit
def group_satellites(tle_path, num_groups=40, group_size=12):
    """
    Function to group satellites from a TLE file into specified number of groups.

    :param tle_path: Path to the TLE file.
    :param num_groups: Number of groups to divide the satellites into.
    :param group_size: Number of satellites in each group.
    :return: Dictionary with satellite names as keys and their group as values.
    """
    # Read TLE file
    with open(tle_path, 'r') as file:
        lines = file.readlines()

    # Initialize group dictionary
    satellite_groups = {}
    for i in range(num_groups):
        for j in range(group_size):
            satellite_index = i * group_size * 3 + j * 3
            if satellite_index < len(lines):
                satellite_name = lines[satellite_index].strip()
                group_name = f'Group {i+1}'
                satellite_groups[satellite_name] = group_name

    return satellite_groups

# Call the function and get the groups
tle_file_path = 'guowang_tle.txt'
satellite_groups = group_satellites(tle_file_path)

# Displaying a portion of the result for verification
print(list(satellite_groups.items())[:])  # Displaying first 15 items as an example