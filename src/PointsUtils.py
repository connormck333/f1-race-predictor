def get_points_by_position(position):
    if position == r"\N":
        return 0

    return 21 - int(position)