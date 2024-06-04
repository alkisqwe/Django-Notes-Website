from django import template

register = template.Library()

@register.filter(name='index')
def index(sequence, position):
    return sequence[position]

@register.simple_tag(name="pagecalc")
def pagecalc_tag(original, end, form):
    revalue = ((original+(end-original))-9)+form
    return revalue
    
@register.simple_tag(name="pagecalc2")
def pagecalc2_tag(original, form):
    revalue = (original-5)+form
    return revalue
