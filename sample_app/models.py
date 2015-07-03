from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    #required field
    user = models.OneToOneField(User, related_name="profile")
    
    sciper = models.CharField(max_length=100, null=True, blank=True)
    where = models.CharField(max_length=100, null=True, blank=True)
    units = models.CharField(max_length=300, null=True, blank=True)
    group = models.CharField(max_length=150, null=True, blank=True)
    classe = models.CharField(max_length=100, null=True, blank=True)
    statut = models.CharField(max_length=100, null=True, blank=True)
    memberof = models.CharField(max_length=300, null=True, blank=True)
    
    def __unicode__(self):
        return """  Sciper:    %s
                    where:     %s
                    units:     %s
                    group:     %s
                    classe:    %s
                    statut:    %s
                    memberof:  %s
                """ % (self.sciper,
                       self.where,
                       self.units,
                       self.group,
                       self.classe,
                       self.statut,
                       self.memberof
                       )
                
#Trigger for creating a profile on user creation 
def user_post_save(sender, instance, **kwargs):
    profile, new = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)                