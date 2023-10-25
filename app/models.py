from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase

from accounts.models import User, Profile
from note import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class NoteQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(created_by=user)


class NoteModel(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = ("active", _("active"))
        HIDDEN = ("hidden", _("hidden"))
        DEACTIVE = ("deactive", _("deactive"))

    title = models.CharField(max_length=100)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ManyToManyField("Category")
    # tag = models.CharField(max_length=100, null=True, blank=True)
    periority = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DEACTIVE)
    allowed_users = models.ManyToManyField(User, blank=True, related_name="allowed_user")
    duedate = models.DateTimeField(null=True, blank=True)
    alerttime = models.DateTimeField(null=True, blank=True)
    objects = NoteQuerySet.as_manager()
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Note"


class Category(BaseModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    parent_category = models.ForeignKey("self", on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    class Status(models.TextChoices):
        PENDING = ('pending', _('pending'))
        APPROVED = ('approved', _('approved'))
        REJECTED = ('rejected', _('rejected'))

    star = models.FloatField(default=0)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(NoteModel, on_delete=models.CASCADE, related_name="comment")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    objects = NoteQuerySet.as_manager()

    def __str__(self):
        return self.created_by.email


class MediaModel(BaseModel):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    media = models.FileField(upload_to=settings.MEDIA_URL)
    note = models.ForeignKey(NoteModel, on_delete=models.CASCADE, related_name='media', null=True)
    size = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Media"


class AddressModel(BaseModel):
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    note = models.ForeignKey(NoteModel, on_delete=models.CASCADE, related_name='address', unique=True)

    class Meta:
        verbose_name = "Address"

    def __str__(self):
        return f"note {self.note.id} address"
