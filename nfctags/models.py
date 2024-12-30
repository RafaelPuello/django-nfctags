import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .validators import validate_ascii_mirror_uid


class NFCTagManager(models.Manager):

    def for_user(self, user=None, active=True):
        """
        Get a queryset of NFC tags instances for a given user.
        """
        if user is None:
            return self.none()
        return self.filter(user=user, active=active)


class NFCTag(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        unique=True
    )
    uid = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        editable=False,
        validators=[validate_ascii_mirror_uid]
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False,
        related_name='nfc_tags'
    )
    active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = NFCTagManager()

    def __str__(self):
        return f"NFC Tag: {self.uid}"

    def __gt__(self, other):
        return self.uid > other.uid

    def __lt__(self, other):
        return self.uid < other.uid

    class Meta:
        ordering = ['uid']
        verbose_name = _("NFC Tag")
        verbose_name_plural = _("NFC Tags")


class NFCTaggableModel(models.Model):
    nfc_tag = models.OneToOneField(
        NFCTag,
        null=True,
        on_delete=models.CASCADE,
        related_name='linked_item'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
