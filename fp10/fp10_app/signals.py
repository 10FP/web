from .models import Student_card
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Student_card())
def activate_user(sender, instance, created, **kwargs):
    print("fp")
    if created and not instance.student_owner:
        
        instance.student_owner = instance.uploaded_by
        print(instance.uploaded_by)
        instance.save