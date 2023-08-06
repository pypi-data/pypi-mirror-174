from setuptools import setup, find_packages

setup(
    name="pyipcore",
    version="0.3.0",
    author="eaglebaby",
    author_email="2229066748@qq.com",
    description="(Only Windows) pyipcore = python (pseudo) (verilog) IP core (rebuilder). Properly adjust your own. v file as an open source IP core, so that it can be easily reconfigured to new projects. Console cmd: 'ipc_rb' and 'ipc_ui'",

    #url="http://iswbm.com/", 

    packages=find_packages(),
    platforms = "",
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
    ],

    install_requires=['pyperclip', "files3", "pyverilog==1.3.0", "pillow", "PyQt5==5.15.6"],

    python_requires='>=3',

    entry_points = {
        'console_scripts': [
            'ipc_rb = pyipcore.ipg:IPRebuild',
            'ipc_ui = pyipcore.ipui_main:UI_IPRebuild',
        ]
    },

)