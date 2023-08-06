
def print_with_failure_style(msg):
    print(msg)


def print_with_success_style(msg):
    print(msg)


def check_compat():
    import platform
    import sys
    v_tuple = platform.python_version_tuple()
    # v_tuple = "3.6.0".split(".")
    v_tuple = tuple(map(lambda x: int(x), v_tuple))
    v = sys.version  # sys.version_info
    if (3, 11, -1) < v_tuple:
        print_with_failure_style(
            f"Your python version is {v}. This program may break because it is currently only compatible with versions between 3.7 and 3.11")
        return False
    elif (3, 7, 0) > v_tuple:
        print_with_failure_style(
            f"Your python version is {v}. This program may break because it is currently only compatible with versions between 3.7 and 3.11")
        return False
    else:
        # print_with_success_style(
        #     f"Your python version is {v} This program was tested with this version and runs properly. However, "
        #     f"if you notice a bug or if your version breaks at runtime please feel free to open a PR on github.")
        return True


#
# if not check_compat():
#     import sys
#
#     sys.exit(0)
