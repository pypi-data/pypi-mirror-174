import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.6.0.post161"
version_tuple = (0, 6, 0, 161)
try:
    from packaging.version import Version as V
    pversion = V("0.6.0.post161")
except ImportError:
    pass

# Data version info
data_version_str = "0.6.0.post19"
data_version_tuple = (0, 6, 0, 19)
try:
    from packaging.version import Version as V
    pdata_version = V("0.6.0.post19")
except ImportError:
    pass
data_git_hash = "727c573ee721025e8bb9cef5a7d26b15811c3676"
data_git_describe = "0.6.0-19-g727c573e"
data_git_msg = """\
commit 727c573ee721025e8bb9cef5a7d26b15811c3676
Merge: 057c0cd8 011baa6c
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed Nov 2 12:15:40 2022 +0100

    Merge pull request #694 from silabs-oysteink/silabs-oysteink_ptr-mcause-stall
    
    CSR stall on CLIC pointers writing to mcause.minhv

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
