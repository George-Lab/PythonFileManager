import os

# function used for tree view mode, level defines
# the depth view
def walk_level(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for cur_root, dirs, files in os.walk(some_dir):
        yield cur_root, dirs, files
        num_sep_this = cur_root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]
