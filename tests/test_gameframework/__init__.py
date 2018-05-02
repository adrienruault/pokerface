# I don't really understand why those commands are that important
# If I remove them the tests are no longer able to find gameframework
# But it seems to only add '/src' to the sys.path so I don't know how it helps
# finding gameframework
import sys
sys.path.append(sys.path[0] + "/src")
