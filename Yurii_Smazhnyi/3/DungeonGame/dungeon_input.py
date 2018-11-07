COMMANDS_TYPES = ("left", "right", "down", "up", "save", "load")


def get_direction():
    """
    Get direction from player.

    :returns: one of valid direction from COMMANDS_TYPES.
    :rtype: str.
    """

    while True:

        direction = input("input command:")

        if direction in COMMANDS_TYPES:
            
            return direction
