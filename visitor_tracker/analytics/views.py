import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import VisitorLog

def home_view(request):
    return render(request, 'index.html')

@csrf_exempt
def update_browser_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            verified_browser = data.get('browser')
            verified_os = data.get('os')
            verified_device = data.get('device')

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', '')

            # Ignore favicon.ico calls to match the actual page hit
            latest_log = VisitorLog.objects.filter(ip_address=ip).exclude(path='/favicon.ico').order_by('-timestamp').first()

            if latest_log:
                if verified_browser:
                    latest_log.browser = verified_browser
                if verified_os:
                    latest_log.operating_system = verified_os
                if verified_device:
                    latest_log.device_type = verified_device
                latest_log.save()

                # UNIFIED CLEAN TERMINAL OUTPUT
                visitor_name = latest_log.user.username if latest_log.user else "Anonymous"
                print("\n" + "="*50)
                print(f"📥 NEW VISITOR LOG DETECTED")
                print(f"   • IP Address : {ip}")
                print(f"   • Visitor    : {visitor_name}")
                print(f"   • Device     : {latest_log.device_type}")
                print(f"   • OS / Browser: {latest_log.operating_system} | {latest_log.browser}")
                print(f"   • Path Hit   : [{latest_log.method}] {latest_log.path}")
                print("="*50 + "\n")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=405)