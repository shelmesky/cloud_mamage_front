from django import template

register = template.Library()


@register.inclusion_tag('tag/paginator_bar.html', takes_context=False)
def render_paginator_bar(paginator,keyword="",start_time="",end_time="",critical="",warning="",unknown=""):
    current = int(paginator.number)
    total = int(paginator.paginator.num_pages)
    
    padding = 9/2
    
    left_part = range(current-padding if current-padding>=1 else 1, current)
    right_part = range(current+1, current+padding+1 if current+padding<=total else total+1)
    
    # try to adjust number of bars to meet PAGINATOR_BAR_NUMBER
    if len(left_part) + len(right_part) + 1 < total:
        if len(left_part) < padding:
            plus = padding - len(left_part)
            right_part = range(current+1, current+padding+plus+1 if current+padding+plus<=total else total+1)
        elif len(right_part) < padding:
            plus = padding - len(right_part)
            left_part = range(current-padding-plus if current-padding-plus>=1 else 1, current)
    
    left_part.append(current)
    left_part.extend(right_part)
    
    if keyword or start_time or end_time or critical or warning or unknown:
        return {
                'paginator': paginator,
                'page_bars': left_part,
                'keyword':keyword,
                'starttime':start_time,
                'endtime':end_time,
                'critical':critical,
                'warning':warning,
                'unknown':unknown
                }
    else:
        return {
                'paginator': paginator,
                'page_bars': left_part, 
        }