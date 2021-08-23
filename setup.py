"""Setup for iframe XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='smowlcheckreg-id-xblock',
    version='70.3',
    description='SMOWL CHECK REGISTER',
    packages=[
        'smowlcheckreg',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'smowlcheckreg = smowlcheckreg:IframeWithAnonymousIDXBlock',
        ],
        "lms.djangoapp": [
            "smowlcheckreg = smowlcheckreg.apps:SmowlCheckRegConfig",
        ],
        "cms.djangoapp": [
            "smowlcheckreg = smowlcheckreg.apps:SmowlCheckRegConfig",
        ]
    },
    package_data=package_data(
        "smowlcheckreg", ["static", "templates", "public"]),
)
