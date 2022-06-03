from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Article, Journal


@receiver(pre_save, sender=Article)
def save_article_impact_factor(sender, instance, **kwargs):
    """Save the sender's 'impact_factor' field based on the related journal."""
    if not instance.locked:
        instance.impact_factor = instance.journal.impact_factor


@receiver(pre_save, sender=Article)
def save_article_points(sender, instance, **kwargs):
    """Save the sender's 'points' field based on the related journal."""
    if not instance.locked:
        instance.points = instance.journal.points


@receiver(post_save, sender=Journal)
def update_articles(sender, instance, **kwargs):
    """
    Update all the unlocked articles published in the journal.

    No further action is needed beside saving of the articles.
    Indeed, the updates are handled by the pre_save signals sent by the article.
    """
    unlocked_articles = Article.objects.filter(journal=instance, locked=False)
    for article in unlocked_articles:
        article.save()
