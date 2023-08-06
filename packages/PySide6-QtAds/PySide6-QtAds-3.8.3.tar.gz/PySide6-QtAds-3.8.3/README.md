# PySide6-QtAds
PySide6 bindings to [Qt Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System)

Pre-built wheels are available for Windows, macOS, and Linux. You can install with:

```
pip install PySide6-QtAds
```

You may also build from source. Example build from source on Ubuntu 22.04:

```bash
# Install Qt (e.g. with aqtinstall) to ~/Qt
LD_LIBRARY_PATH=~/Qt/6.4.0/gcc_64/lib \
CMAKE_PREFIX_PATH=~/Qt/6.4.0/gcc_64/lib/cmake/ \
PIP_EXTRA_INDEX_URL=https://download.qt.io/official_releases/QtForPython/ \
pip install -v .
```

Note: `shiboken6-generator` is required when building from source, and currently only available via Qt's package index.

# Examples
https://github.com/mborgerson/Qt-Advanced-Docking-System/tree/pyside6

# Credits
- Original PySide6 binding work by CJ Niemira via https://github.com/cniemira/pyside6_qtads
- With bindings.xml improvements via https://github.com/metgem/PySide2Ads
