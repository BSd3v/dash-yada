from __future__ import print_function as _
from ._imports_ import *
from ._imports_ import __all__
import os as _os
import sys as _sys
import json

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, "package-info.json"))
with open(_filepath) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")
__version__ = package["version"]

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]

_unpkg = f"https://unpkg.com/dash-yada@{__version__}/dash_yada/"

_js_dist = [
    {
        "relative_package_path": "yada.js",
        "external_url": f"{_unpkg}yada.js",
        "namespace": package_name,
    },
]

_css_dist = [
    {
        "relative_package_path": "yada.css",
        "external_url": f"{_unpkg}yada.css",
        "namespace": package_name,
    },
    {
        "relative_package_path": "tech-support.png",
        "external_url": f"{_unpkg}tech-support.png",
        "namespace": package_name,
    },
{
        "relative_package_path": "yada.png",
        "external_url": f"{_unpkg}yada.png",
        "namespace": package_name,
    },
{
        "relative_package_path": "yada_headshot.png",
        "external_url": f"{_unpkg}yada_headshot.png",
        "namespace": package_name,
    },
{
        "relative_package_path": "yada.gif",
        "external_url": f"{_unpkg}yada.gif",
        "namespace": package_name,
    },
]


for _component in __all__:
    setattr(locals()[_component], "_js_dist", _js_dist)
    setattr(locals()[_component], "_css_dist", _css_dist)
