import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .validators import validate_ascii_mirror_uid

User = get_user_model()


class NFCTagBatch(models.Model):
    """
    Model to group NFCTags together for batch management.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Batch Name"),
        help_text=_("A descriptive name for this batch of NFC Tags.")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Optional description for this batch.")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nfc_tag_batches',
        verbose_name=_("User"),
        help_text=_("The user of this batch.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("NFC Tag Batch")
        verbose_name_plural = _("NFC Tag Batches")


class NFCTagManager(models.Manager):

    def for_user(self, user=None, active=True):
        """
        Get a queryset of NFC tags instances for a given user.
        """
        if user is None:
            return self.none()
        return self.filter(batch__user=user, active=active)


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
    batch = models.ForeignKey(
        NFCTagBatch,
        on_delete=models.CASCADE,
        editable=False,
        related_name='nfc_tags'
    )
    content = models.JSONField(
        default=dict
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
