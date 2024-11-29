from django.shortcuts import render



# Create your views here.
def Home(request):
    return render(request, 'faq/faq.html', {'show_footer': True})
