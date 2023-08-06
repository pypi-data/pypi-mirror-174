from cms.models import CMSPlugin
from django.db import models
from filer.fields.image import FilerImageField


class ContentWidthImage(CMSPlugin):
    """
    Represents an image object
    """

    image = FilerImageField(
        related_name="+",
        verbose_name="Content Width Image",
        on_delete=models.SET_NULL,
        null=True,
    )
    caption = models.CharField(
        max_length=255, help_text="Add a caption to the image", blank=True, default=""
    )
    alt_text = models.CharField(max_length=64, help_text="Image name", default="")
    credit = models.CharField(max_length=255)

    def __str__(self):
        """
        String representation of the object
        """
        return f"Content Width Image {self.pk}"
