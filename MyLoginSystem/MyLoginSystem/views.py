from django.shortcuts import render

def catch_url_data_view(request):
    # 1. Look for the 'name' key inside the request.GET dictionary
    user_name = request.GET.get('name', '')
    
    # 2. Pack it into the context basket
    basket = {
        'display_name': user_name,
    }
    
    # 3. Render the HTML page and hand it the basket
    return render(request, 'form_gate.html', basket)