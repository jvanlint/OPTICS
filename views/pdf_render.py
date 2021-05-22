from django.http import HttpResponse
from ..models import Mission, Flight
# For PDF
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# PDF Render

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def download_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)

    data = {'mission_object': mission, 'flight_object': flight}
    pdf = render_to_pdf('mission_card/pdf_template.html', data)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "missioncard.pdf"
    content = "attachment; filename=%s" % (filename)
    response['Content-Disposition'] = content
    return response


def view_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)

    data = {'mission_object': mission, 'flight_object': flight}

    pdf = render_to_pdf('mission_card/pdf_template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')