from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from ..models import Mission, Flight


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def download_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)

    data = {"mission_object": mission, "flight_object": flight}
    pdf = render_to_pdf("mission_card/pdf_template.html", data)
    response = HttpResponse(pdf, content_type="application/pdf")
    filename = "missioncard.pdf"
    content = "attachment; filename=%s" % (filename)
    response["Content-Disposition"] = content
    return response


def view_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)
    packages = mission.package_set.all()
    aircraft = flight.aircraft_set.all().order_by("-flight_lead")
    waypoints = flight.waypoint_set.all()
    supports = mission.support_set.all()
    targets = flight.targets.all()
    threats = mission.threat_set.all()
    # threat_details = threats.threat_name.harm_code

    target_urls = []
    if targets:
        for target in targets:
            if target.target_image:
                target_urls.append(request.build_absolute_uri(target.target_image.url))

    data = {
        "mission_object": mission,
        "flight_object": flight,
        "packages_object": packages,
        "aircraft_object": aircraft,
        "waypoints_object": waypoints,
        "support_object": supports,
        "target_object": targets,
        "threat_object": threats,
        "urls": target_urls,
    }

    # pdf = render_to_pdf("mission_card/pdf_template.html", data)
    pdf = render_to_pdf("mission_card/mission_card_2.html", data)
    return HttpResponse(pdf, content_type="application/pdf")
