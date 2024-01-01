from django.conf import settings
# import signals
from django.db.models.signals import post_save
# import decorator
from django.dispatch import receiver
from .models import Customer

# Das Signal wird ausgelöst, wenn ein Objekt des Modells AUTH_USER_MODEL gespeichert wird
# param "sender" is: sender ist die Modellklasse, die das Signal gesendet hat (in diesem Fall das core.user)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        # kwargs["instance"] ist die Instanz des Benutzermodells, das gerade gespeichert wurde.
        Customer.objects.create(user=kwargs["instance"])
