def get_ctx_result(provides, result):

    ctx_result = {}
    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result['param'] = param
    ctx_result['action'] = provides

    if data:
        ctx_result['data'] = data

    if summary:
        ctx_result['summary'] = summary

    return ctx_result


def display_view(provides, all_app_runs, context):

    context['results'] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:

            ctx_result = get_ctx_result(provides, result)
            if (not ctx_result):
                continue
            results.append(ctx_result)

    if provides == "list managed devices":
        return_page = "microsoftintune_list_devices.html"

    return return_page
