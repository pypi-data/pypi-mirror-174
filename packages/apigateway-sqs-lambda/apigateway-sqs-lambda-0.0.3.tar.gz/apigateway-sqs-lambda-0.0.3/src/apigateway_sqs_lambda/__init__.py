'''
# apigateway-sqs-lambda

CDK Construct for standard apigateway-sqs-lambda functionality
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_apigateway
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sqs
import constructs


class ApiGatewayToSqsToLambda(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="apigateway-sqs-lambda.ApiGatewayToSqsToLambda",
):
    '''
    :stability: experimental
    :summary:

    The ApiGatewayToSqsToLambda class. Class is very opinionated and does not allow for existing queues or lambdas.
    Class assumes a pulic domain should be created and the corresponding alias in route53 shall be created
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        domain: builtins.str,
        domain_cert_arn: builtins.str,
        lambda_function_props: typing.Union[aws_cdk.aws_lambda.FunctionProps, typing.Dict[str, typing.Any]],
        route53_hosted_zone_id: builtins.str,
        service_name: builtins.str,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param domain: 
        :param domain_cert_arn: 
        :param lambda_function_props: 
        :param route53_hosted_zone_id: 
        :param service_name: 
        :param deploy_dead_letter_queue: 

        :stability: experimental
        :summary: Constructs a new instance of the ApiGatewayToSqsToLambda class.
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                domain: builtins.str,
                domain_cert_arn: builtins.str,
                lambda_function_props: typing.Union[aws_cdk.aws_lambda.FunctionProps, typing.Dict[str, typing.Any]],
                route53_hosted_zone_id: builtins.str,
                service_name: builtins.str,
                deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApiGatewayToSqsToLambdaProps(
            domain=domain,
            domain_cert_arn=domain_cert_arn,
            lambda_function_props=lambda_function_props,
            route53_hosted_zone_id=route53_hosted_zone_id,
            service_name=service_name,
            deploy_dead_letter_queue=deploy_dead_letter_queue,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> aws_cdk.aws_apigateway.RestApi:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_apigateway.RestApi, jsii.get(self, "apiGateway"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayRole")
    def api_gateway_role(self) -> aws_cdk.aws_iam.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "apiGatewayRole"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.Queue:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_sqs.Queue, jsii.get(self, "sqsQueue"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayCloudWatchRole")
    def api_gateway_cloud_watch_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_iam.Role], jsii.get(self, "apiGatewayCloudWatchRole"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue], jsii.get(self, "deadLetterQueue"))


@jsii.data_type(
    jsii_type="apigateway-sqs-lambda.ApiGatewayToSqsToLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "domain_cert_arn": "domainCertArn",
        "lambda_function_props": "lambdaFunctionProps",
        "route53_hosted_zone_id": "route53HostedZoneId",
        "service_name": "serviceName",
        "deploy_dead_letter_queue": "deployDeadLetterQueue",
    },
)
class ApiGatewayToSqsToLambdaProps:
    def __init__(
        self,
        *,
        domain: builtins.str,
        domain_cert_arn: builtins.str,
        lambda_function_props: typing.Union[aws_cdk.aws_lambda.FunctionProps, typing.Dict[str, typing.Any]],
        route53_hosted_zone_id: builtins.str,
        service_name: builtins.str,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param domain: 
        :param domain_cert_arn: 
        :param lambda_function_props: 
        :param route53_hosted_zone_id: 
        :param service_name: 
        :param deploy_dead_letter_queue: 

        :stability: experimental
        :summary: The properties for the ApiGatewayToSqsToLambdaProps class.
        '''
        if isinstance(lambda_function_props, dict):
            lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        if __debug__:
            def stub(
                *,
                domain: builtins.str,
                domain_cert_arn: builtins.str,
                lambda_function_props: typing.Union[aws_cdk.aws_lambda.FunctionProps, typing.Dict[str, typing.Any]],
                route53_hosted_zone_id: builtins.str,
                service_name: builtins.str,
                deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument domain_cert_arn", value=domain_cert_arn, expected_type=type_hints["domain_cert_arn"])
            check_type(argname="argument lambda_function_props", value=lambda_function_props, expected_type=type_hints["lambda_function_props"])
            check_type(argname="argument route53_hosted_zone_id", value=route53_hosted_zone_id, expected_type=type_hints["route53_hosted_zone_id"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument deploy_dead_letter_queue", value=deploy_dead_letter_queue, expected_type=type_hints["deploy_dead_letter_queue"])
        self._values: typing.Dict[str, typing.Any] = {
            "domain": domain,
            "domain_cert_arn": domain_cert_arn,
            "lambda_function_props": lambda_function_props,
            "route53_hosted_zone_id": route53_hosted_zone_id,
            "service_name": service_name,
        }
        if deploy_dead_letter_queue is not None:
            self._values["deploy_dead_letter_queue"] = deploy_dead_letter_queue

    @builtins.property
    def domain(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_cert_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("domain_cert_arn")
        assert result is not None, "Required property 'domain_cert_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_function_props(self) -> aws_cdk.aws_lambda.FunctionProps:
        '''
        :stability: experimental
        '''
        result = self._values.get("lambda_function_props")
        assert result is not None, "Required property 'lambda_function_props' is missing"
        return typing.cast(aws_cdk.aws_lambda.FunctionProps, result)

    @builtins.property
    def route53_hosted_zone_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("route53_hosted_zone_id")
        assert result is not None, "Required property 'route53_hosted_zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deploy_dead_letter_queue(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deploy_dead_letter_queue")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiGatewayToSqsToLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApiGatewayToSqsToLambda",
    "ApiGatewayToSqsToLambdaProps",
]

publication.publish()
