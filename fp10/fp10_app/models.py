from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from .studentCardProccesing import imageToString, translateEnglishToTurkish, cleanString, aiModel
from PIL import Image
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model_path = "fp10_app/ai_model/best-3.pt"
# Create your models here.
class CustomUser(AbstractUser):
    
    online_status = models.BooleanField(default=False, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    job = models.TextField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    is_email_verified = models.BooleanField(default=False)
    last_username_change_date = models.DateTimeField(null=True, blank=True)
    verification_code = models.IntegerField(null=True, blank=True)
    student_number = models.PositiveIntegerField(default=0)
    student_department = models.CharField(max_length=100, default="a")

class Student_card(models.Model):
    student_owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True)
    student_card = models.ImageField(upload_to='student_card/')

    def __str__(self) -> str:
        return f"{self.student_owner}"
    
class Activity(models.Model):
    title = models.CharField(max_length=200)  
    text = models.TextField()  
    picture = models.ImageField(upload_to='activities/', null=True, blank=True)  
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_activities') 
    partitions = models.ManyToManyField(CustomUser, related_name='participating_activities', blank=True)  
    start_time = models.DateTimeField(null=True, blank=True)  
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['start_time']  

    def is_past_due(self):
        from django.utils import timezone
        return self.end_time < timezone.now()



@receiver(post_save, sender=Student_card)
def set_user_as_poster(sender, instance, created, **kwargs):
    if created:
        if instance.student_owner:
            (student_name, student_number) = imageToString(instance.student_card)
            full_name = f"{instance.student_owner.first_name} {instance.student_owner.last_name.upper()}"
            user_ = translateEnglishToTurkish(cleanString(full_name.strip()))
            card_ = translateEnglishToTurkish(cleanString(student_name.strip()))
            
            if user_.strip() == card_.strip():

                if int(instance.student_owner.student_number) == int(student_number):
                    instance.student_owner.is_email_verified = True
                    instance.student_owner.save()
            
            if aiModel(model=model_path, image=f"uploads/{str(instance.student_card)}", name=user_.strip().replace(" ", "")):
                image_path = user_.strip().replace(" ", "")
                print(image_path)
                pp_path = str(instance.student_card).replace("student_card/", "").replace(".jpeg", ".jpg")
                old_path = f"{BASE_DIR}/uploads/profile_pics/{image_path}/predict/crops/face/{pp_path}"
                target_path = f"{BASE_DIR}/uploads/profile_pics/{pp_path}"
                shutil.move(old_path, target_path)
                print(BASE_DIR)
                x = pp_path.replace("jpeg", "jpg")
                instance.student_owner.profile_picture = f"profile_pics/{x}"
                instance.student_owner.save()
            


            



