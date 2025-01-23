from django.db import models
from django.db.models import Q


class BaseModel(models.Model):
    """
    Base model for all models in the project with some common fields and methods.
    The structure to be followed by all models throughout the project is as follows:
    - Add a white space after every category of fields definition.
    - Foreign key fields should be defined at the top of the model.
    - Then the common fields except the boolean fields should be defined.
    - Then the boolean fields (flags) should be defined.
    - Then many-to-many fields should be defined.
    - Then the Meta class should be defined.
    - Then the methods should be defined.
    """

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def get_random(cls, count: int | None = None, q_filter: Q | None = Q(), annotation: dict = {}):
        qs = cls.objects.annotate(**annotation).filter(q_filter).order_by("?")
        if count:
            return qs[:count]
        return qs
