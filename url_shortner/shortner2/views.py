from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.views import View
from .models import SjURL
from .forms import SubmitUrlForm
from analytics.models import ClickEvent

def home_view_fbv(request, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
    return render(request, "shortner2/home.html", {})


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "WWW.SJ.COM",
            "form": the_form
        }
        return render(request, "shortner2/home.html", context) 

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "WWW.SJ.COM",
            "form": form
        }
        template='shortner2/home.html'
        if form.is_valid():
            print(form.cleaned_data.get("url"))
            new_url=form.cleaned_data.get("url")
            obj, created = SjURL.objects.get_or_create(url=new_url)
            print created
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortner2/success.html"
            else:
                template = "shortner2/exists.html"


        return render(request, template,context)

# def sj_redirect_view(requests,shortcode=None,*args,**kwargs):
	
# 	obj= get_object_or_404(SjURL,shortcode=shortcode)
# 	print(obj.url)
# 	# obj_url=None
# 	# qs= SjURL.objects.filter(shortcode_iexact=shortcode)
# 	# if qs.exists() and qs.count()==1:
# 	# 	obj=qs.first()
# 	# 	obj_url=obj.url
# 	return HttpResponseRedirect(obj.url)

class URLRedirectView(View):
    def get(self,requests,shortcode=None,*args,**kwargs):
        qs=SjURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print (obj)
        print(ClickEvent.objects.create_event(obj))
        print(obj.url)
        url2=obj.url
        return HttpResponseRedirect('http://'+url2)
	# def post(self,requests,*args,**kwargs):
	# 	obj= get_object_or_404(SjURL,shortcode=shortcode)
		
	# 	return HttpResponseRedirect(obj.url)