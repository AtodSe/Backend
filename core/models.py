from django.db import models
from django.utils.timezone import now

class SoftDeleteManager(models.Manager):
    """
    Manager class for SoftDeleteModel
    
    include objects where the deleted_at field is NULL
    """
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def delete(self):
        self.deleted_at = now()
        return self.save()

    def restore(self):
        self.deleted_at = None
        return self.save()

    class Meta:
        abstract=True

