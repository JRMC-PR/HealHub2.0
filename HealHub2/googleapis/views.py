from django.shortcuts import render

# Create your views here.
def search_doctors(request):
    # You can include logic here to process any server-side search requirements
    # For example, you might log search queries to your database

    return render(request, 'googleapis/search_doctors.html')
