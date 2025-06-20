from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .tasks import process_reported_host


@csrf_exempt
def hostname_view(request):
    """API entry point for reporting hostnames"""
    if request.method == "POST":
        data = json.loads(request.body)
        hostname = data["hostname"]
        source = data["source"]
        process_reported_host.delay(hostname, source)
        print(f"Processed hostname from API: {hostname}", flush=True)
        return JsonResponse({"status": "queued", "hostname": hostname}, status=202)
    else:
        return JsonResponse({"error": "Only POST allowed"}, status=405)
