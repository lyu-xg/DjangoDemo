from django.shortcuts import render

# Create your views here.
def venues(request):
    return render(request, "templates/venues.html", {})