try:
    # noinspection PyShadowingBuiltins
    from printlog import printlog as print
except ImportError:
    pass

try:
    import CONFIG_CV_SERVER
    is_Server = True
except ImportError:
    is_Server = False

try:
    import CONFIG_CV_ROBOT
    is_Robot = True
except ImportError:
    is_Robot = False

print("CV Robot version 0.1.4")
if is_Robot:
    print("Running on robot...")
elif is_Server:
    print("Running on server...")
else:
    print("Running in emulation mode...")