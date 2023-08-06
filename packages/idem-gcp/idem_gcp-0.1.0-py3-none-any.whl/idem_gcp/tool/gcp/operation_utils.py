async def handle_operation(hub, ctx, operation_id, resource_type: str):
    operation_result = {
        "comment": [],
        "result": True,
        "rerun_data": None,
        "resource_id": None,
    }

    get_ret = await hub.exec.gcp.compute.zoneOperations.get(
        ctx, resource_id=operation_id
    )

    if not get_ret["result"] or not get_ret["ret"]:
        operation_result["result"] = False
        operation_result["comment"] = get_ret["comment"]
        return operation_result

    if get_ret["ret"]["status"] != "DONE":
        operation_result["result"] = False
        operation_result[
            "rerun_data"
        ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            get_ret["ret"].get("selfLink"), "compute.zoneOperations"
        )
        operation_result["comment"] += get_ret["comment"]
        return operation_result

    if get_ret["ret"].get("error"):
        operation_result["result"] = False
        operation_result["comment"] += str(get_ret["ret"].get("error", {}))
        return operation_result

    operation_result[
        "resource_id"
    ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
        get_ret["ret"].get("targetLink"), resource_type
    )

    return operation_result
