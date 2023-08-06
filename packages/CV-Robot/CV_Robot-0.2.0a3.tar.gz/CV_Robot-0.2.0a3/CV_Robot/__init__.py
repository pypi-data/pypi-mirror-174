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
    import CONFIG_CV_LIVE_IMG
    useLiveImg = True
except ImportError:
    useLiveImg = False

try:
    import CONFIG_CV_ROBOT
    is_Robot = True
except ImportError:
    is_Robot = False

print("CV Robot version 0.2.0 Alpha 3")
if is_Robot:
    print("Running on robot...")
elif is_Server:
    print("Running on server...")
else:
    print("Running in emulation mode...")