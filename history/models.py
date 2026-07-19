from django.db import models
from django.conf import settings
from listings.models import Listing

class SearchHistory(models.Model):
    """
    Model representing user search history.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='search_history', null=True, blank=True)
    query_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Search: '{self.query_text}' by {self.user or 'Guest'}"

class ViewHistory(models.Model):
    """
    Model representing user view history for listings.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='view_history', null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"Viewed Listing #{self.listing.id} by {self.user or 'Guest'}"