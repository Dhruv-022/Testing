import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import VisitorLog

@csrf_exempt
def update_browser_info(request):
    """
    v2.0 Endpoint: Receives verified client-side browser & OS data from JS
    and updates the latest VisitorLog entry for the requesting IP.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            verified_browser = data.get('browser')
            verified_os = data.get('os')

            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR', '')

            # Fetch the most recent log created by middleware for this IP
            latest_log = VisitorLog.objects.filter(ip_address=ip).order_by('-timestamp').first()

            if latest_log and (verified_browser or verified_os):
                old_browser = latest_log.browser
                old_os = latest_log.operating_system

                if verified_browser:
                    latest_log.browser = verified_browser
                if verified_os:
                    latest_log.operating_system = verified_os

                latest_log.save()

                # v2.0 Live Terminal Override Log
                print("\n" + "✨"*25)
                print(f"🎯 v2.0 CLIENT VERIFICATION OVERRIDE")
                print(f"   • IP Address       : {ip}")
                print(f"   • Server Header OS : {old_os} | Browser: {old_browser}")
                print(f"   • JS Verified OS   : {latest_log.operating_system} | Browser: {latest_log.browser}")
                print("✨"*25 + "\n")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=405)

from django.shortcuts import render

def home_view(request):
    return render(request, 'index.html')