from django.template.loader import get_template
from django.template import Context

def render_email_content(up, outage):

	if not up:
		template = 'email/start.html'
	elif up:
		template = 'email/end.html'

	return get_template(template).render(
        Context({
            'outage': outage,
        })
    )