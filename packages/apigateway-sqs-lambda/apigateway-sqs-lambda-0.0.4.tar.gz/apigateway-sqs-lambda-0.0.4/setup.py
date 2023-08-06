import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "apigateway-sqs-lambda",
    "version": "0.0.4",
    "description": "Package provides opinionated constrcut for API Gateway with associated SQS queue and Lambda function",
    "license": "Apache-2.0",
    "url": "https://github.com/FBosler/apigateway-sqs-lambda.git",
    "long_description_content_type": "text/markdown",
    "author": "Fabian<FBosler@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/FBosler/apigateway-sqs-lambda.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "apigateway_sqs_lambda",
        "apigateway_sqs_lambda._jsii"
    ],
    "package_data": {
        "apigateway_sqs_lambda._jsii": [
            "apigateway-sqs-lambda@0.0.4.jsii.tgz"
        ],
        "apigateway_sqs_lambda": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "aws-solutions-constructs.core==2.25.0",
        "constructs>=10.0.5, <11.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
