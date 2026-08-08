class SimpleGreetingMiddleware:
    def __init__(self, get_response):
        # This runs ONCE when the server starts up
        self.get_response = get_response

    def __call__(self, request):
        # 1. CODE HERE RUNS BEFORE THE VIEW
        print("➡️  [Middleware]: Request is passing through!")
        
        # Attach a custom attribute directly to the request object
        request.custom_greeting = "Hello from Middleware!"

        # Pass the request along to the next middleware or view
        response = self.get_response(request)

        # 2. CODE HERE RUNS AFTER THE VIEW
        print("⬅️  [Middleware]: Response is heading back to browser!")

        return response