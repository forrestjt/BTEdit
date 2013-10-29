from distutils.core import setup
import py2exe


setup(
    windows = [
        {
            "script": "BTEdit.py",
            "icon_resources": [(1, "tree.ico")],
        }
    ],
      data_files=["tree.ico"],

)
