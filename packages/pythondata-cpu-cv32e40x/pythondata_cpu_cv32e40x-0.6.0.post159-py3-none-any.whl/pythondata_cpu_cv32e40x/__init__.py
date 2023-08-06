import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.6.0.post159"
version_tuple = (0, 6, 0, 159)
try:
    from packaging.version import Version as V
    pversion = V("0.6.0.post159")
except ImportError:
    pass

# Data version info
data_version_str = "0.6.0.post17"
data_version_tuple = (0, 6, 0, 17)
try:
    from packaging.version import Version as V
    pdata_version = V("0.6.0.post17")
except ImportError:
    pass
data_git_hash = "057c0cd850760bd952528e52289bf4d4f2758dbf"
data_git_describe = "0.6.0-17-g057c0cd8"
data_git_msg = """\
commit 057c0cd850760bd952528e52289bf4d4f2758dbf
Merge: 93bf5453 37ef9460
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Tue Nov 1 13:57:16 2022 +0100

    Merge pull request #693 from silabs-oysteink/minhv-clear-wb
    
    mcause.minhv clear from WB stage

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
