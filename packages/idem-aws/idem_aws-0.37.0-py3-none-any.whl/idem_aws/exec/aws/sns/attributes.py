from typing import Dict

from dict_tools import differ


async def update_topic_attributes(
    hub,
    ctx,
    resource_arn: str,
    old_attributes: Dict[str, str],
    new_attributes: Dict[str, str],
):
    """
    Given old and new attributes of SNS topic the function updates the attributes.

    Args:
        hub:
        ctx:
        resource_arn(Text): AWS resource_arn of SNS topic
        old_attributes(Dict): old attribute of SNS topic
        new_attributes(Dict): new attribute of SNS topic

    """
    result = dict(comment=(), result=True, ret=None)
    json_attributes = [
        "DeliveryPolicy",
        "Policy",
    ]
    attributes_to_update = {}
    for key, value in new_attributes.items():
        if key in old_attributes:
            if key in json_attributes:
                # standardise json strings and check if they are identical else add to update dictionary
                old_value_standardised = (
                    hub.tool.aws.state_comparison_utils.standardise_json(
                        old_attributes.get(key)
                    )
                )
                value_standardised = (
                    hub.tool.aws.state_comparison_utils.standardise_json(value)
                )
                if not hub.tool.aws.state_comparison_utils.is_json_identical(
                    old_value_standardised, value_standardised
                ):
                    attributes_to_update[key] = value
            else:
                # check if other string attributes are equal else add to update dictionary
                if old_attributes.get(key) != value:
                    attributes_to_update[key] = value
        else:
            attributes_to_update[key] = value

    if attributes_to_update:
        if ctx.get("test", False):
            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] = (
                f"Would Update attributes {attributes_to_update.keys()}",
            )
            return result

        else:
            for key, value in attributes_to_update.items():
                ret = await hub.exec.boto3.client.sns.set_topic_attributes(
                    ctx, TopicArn=resource_arn, AttributeName=key, AttributeValue=value
                )
                if not ret["result"]:
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result

            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] = (f"Updated attributes {attributes_to_update.keys()}",)
    return result


async def update_subscription_attributes(
    hub,
    ctx,
    resource_arn: str,
    old_attributes: Dict[str, str],
    new_attributes: Dict[str, str],
):
    """
    Given old and new attributes of SNS topic_subscription the function updates the attributes.

    Args:
        hub:
        ctx:
        resource_arn(Text): AWS resource_arn of SNS topic_subscription
        old_attributes(Dict): old attribute of SNS topic_subscription
        new_attributes(Dict): new attribute of SNS topic_subscription

    """
    result = dict(comment=(), result=True, ret=None)
    attributes_diff = differ.deep_diff(old_attributes, new_attributes)
    attributes_to_update = attributes_diff.get("new")

    if attributes_to_update:
        if ctx.get("test", False):
            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] = (
                f"Would Update attributes {attributes_to_update.keys()}",
            )
            return result

        else:
            for key, value in attributes_to_update.items():
                ret = await hub.exec.boto3.client.sns.set_subscription_attributes(
                    ctx,
                    SubscriptionArn=resource_arn,
                    AttributeName=key,
                    AttributeValue=value,
                )
                if not ret["result"]:
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result

            result["ret"] = {"updated_attributes": attributes_to_update}
            result["comment"] = (f"Updated attributes {attributes_to_update.keys()}",)
    return result
