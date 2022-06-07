from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from authorships.models import Authorship

from .models import Article, Journal


@receiver(post_save, sender=Journal)
def update_unlocked_articles(sender, instance, **kwargs):
    """
    Update all the unlocked articles published in the journal.

    No further action is needed beside saving of the articles. This is due to the
    fact that the update is handled by clean method of the Article model.
    """
    unlocked_articles = Article.objects.filter(journal=instance, locked=False)
    for article in unlocked_articles:
        article.clean()
        article.save()


@receiver([post_save, post_delete], sender=Authorship)
def update_article_authors(sender, instance, **kwargs):
    """Update the authorship-related fields of the Article models."""
    if not instance.content_type == ContentType.objects.get_for_model(Article):
        return

    try:
        article = Article.objects.get(pk=instance.object_id)
    except Article.DoesNotExist:
        return

    authors = article.get_authors()

    article.authors, article.author_count = (
        ", ".join([author.alias for author in authors]),
        len(authors),
    )

    article.save()
