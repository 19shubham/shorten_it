from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from .utils import code_generator,create_shortcode
from .validators import validate_url, validate_dot_com
from django_hosts.resolvers import reverse
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

# Create your models here.
class SjURLManager(models.Manager):
	def all(self,*args,**kwargs):
		qs_main=super(SjURLManager,self).all(*args,**kwargs)
		qs= qs_main.filter(update=True,active=True)
		return qs

	def refresh_shortcodes(self,items=None):
		qs = SjURL.objects.filter(id__gte=1)
		if items is not None and isinstance(items,int):
			qs=qs.order_by('-id')[:items]
		new_codes = 0
		for q in qs:
			q.shortcode = create_shortcode(q)
			print(q.id)
			q.save()
			new_codes += 1
		return "New codes made: {i}".format(i=new_codes)


class SjURL(models.Model):
	url= models.CharField(max_length=220, unique=True,blank=False, validators=[validate_url, validate_dot_com])
	shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True,)
	updated=models.DateTimeField(auto_now=True,)
	timestamp=models.DateTimeField(auto_now_add=True,)
	update=models.BooleanField(default=True,)

	#objects=SjURLManager()
	#some_random=SjURLManager()

	def __str__(self):
		return str(self.url)
	def __unicode__(self):
		return str(self.url)

	def save(self,*args,**kwargs):
		if self.shortcode is None or self.shortcode=="":
			self.shortcode=create_shortcode(self)
		# if not "http" in self.url:
		# 	self.url= "http://" +self.url
		super(SjURL,self).save(*args,**kwargs)

	def get_short_url(self):
		url_path= reverse("scode",kwargs={'shortcode':self.shortcode },host='www',scheme='http')
		return url_path