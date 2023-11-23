from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='tickets')
    time_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.title} | {self.user.username}'

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    #ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='reviews') 
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket.title} | {self.rating} | {self.user.username}'

class UserFollows(models.Model):
    # Your UserFollows model definition goes
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followerd_by',
    )

    def __str__(self):
       return f"{self.user.username} follows {self.followed_user.username}"
    
    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = 'abonnement'
        verbose_name_plural = 'abonnements'


# class profile utilisateur
# class Profile(models.Model):
#     user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True, null=True, default=None)
#     image = models.ImageField(null=True, blank=True, upload_to='profiles', default='default.png')

#     def __str__(self):
#         return f"{self.user.username} profile"
    
#     class Meta:
#         verbose_name = 'profile'
#         verbose_name_plural = 'profiles'

    
