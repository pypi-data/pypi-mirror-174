import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.asset-kubectl-v20",
    "version": "2.1.0",
    "description": "A library that contains kubectl for use in Lambda Layers",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/awscdk-asset-kubectl#readme",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services, Inc.",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/awscdk-asset-kubectl.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.asset_kubectl_v20._jsii"
    ],
    "package_data": {
        "aws_cdk.asset_kubectl_v20._jsii": [
            "asset-kubectl-v20@2.1.0.jsii.tgz"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "jsii>=1.70.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
