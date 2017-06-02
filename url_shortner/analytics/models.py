from django.db import models


from shortner2.models import SjURL


class ClickEventManager(models.Manager):
    def create_event(self, SjInstance):
        if isinstance(SjInstance, SjURL):
            obj, created = self.get_or_create(sj_url=SjInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    sj_url    = models.OneToOneField(SjURL)
    count       = models.IntegerField(default=0)
    updated     = models.DateTimeField(auto_now=True) 
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)