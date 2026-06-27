from django.http import HttpResponse

def catch_url_data_view(request):
    # 1. Inspect the request.GET dictionary object for specific URL string keys
    user_name = request.GET.get('name', 'MissingName')
    user_hobby = request.GET.get('hobby', 'MissingHobby')
    
    # 2. Print the extracted variables directly to your running terminal console
    print("\n" + "="*50)
    print("📡 LIVE NETWORK INTERCEPTION IN PROGRESS...")
    print(f"Captured 'name' from browser bar: {user_name}")
    print(f"Captured 'hobby' from browser bar: {user_hobby}")
    print("="*50 + "\n")
    
    # 3. Ship a basic response back to the client browser layout
    return HttpResponse(f"<h1>Lab Status: Success! Active User: {user_name}</h1>")