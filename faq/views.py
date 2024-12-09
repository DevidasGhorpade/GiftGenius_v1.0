from django.shortcuts import render

# Create your views here.
def display_faq(request):
    return render(request, 'faq/faq.html', {'show_footer': True})