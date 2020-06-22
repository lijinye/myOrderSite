from django import template
from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, results
from django.contrib.admin.templatetags.base import InclusionAdminNode
import re

register = template.Library()


def result_list(cl):
    """
    Display the headers and data list together.
    """
    headers = list(result_headers(cl))
    result = list(results(cl))
    count = 0
    for item in result:
        count_tag = item[-1]
        if count_tag.find('field-count') != -1:
            count = count + int(re.search('\d+', count_tag).group())
    if count > 0:
        headers[-1]['text'] = headers[-1]['text'] + '(本页共计' + str(count) + '份)'
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {
        'cl': cl,
        'result_hidden_fields': list(result_hidden_fields(cl)),
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields,
        'results': result,
    }


@register.tag(name='result_list_new')
def result_list_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=result_list,
        template_name='change_list_results.html',
        takes_context=False,
    )
