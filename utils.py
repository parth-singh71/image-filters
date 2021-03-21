import os


def create_dir(dir):
    """Creates a directory if not already exists

    Args:
        dir (String): path of directory
    """
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Cannot create directory named \"' + dir + '\"')


def get_output_number(dst):
    """Gives the last output folder number

    Returns:
        int: Last output folder number
    """
    data = os.listdir(dst)
    if not data == []:
        last_record = sorted(data)[-1]
        hiphen_index = last_record.rfind("-")
        return int(last_record[hiphen_index + 1:])
    return 0
