from datetime import datetime

from django.db import models

from buscador import utils


class Evaluation(models.Model):
    autority_points = models.FloatField(default=0.0)
    frequency_points = models.FloatField(default=0.0)
    tags_points = models.FloatField(default=0.0)
    auto_reference_penalty = models.FloatField(default=0.0)
    fresh_points = models.FloatField(default=0.0)

    def get_total_points(self):
        return (
            self.autority_points
            + self.frequency_points
            + self.tags_points
            - self.auto_reference_penalty
            + self.fresh_points
        )

    def fresh_evaluation(self, page_date: datetime):
        if page_date is None:
            self.fresh_points = -utils.multiplyers["invalid_date_penalty"]
            return
        # Validação de data:.
        current_date = datetime.now()
        date_difference = int(
            (current_date.date() - page_date.date()).days / 365.25,
        )
        self.fresh_points = (
            utils.multiplyers["fresh_content"]
            - date_difference * utils.multiplyers["fresh_content_penalty"]
        )


class ExternalLink(models.Model):
    url = models.URLField(verbose_name="Link Externo")


class Page(models.Model):
    title = models.CharField(verbose_name="Titulo")
    index = models.URLField(verbose_name="URL da Página")
    date = models.DateField(verbose_name="Data de Publicação", null=True)
    content = models.TextField(verbose_name="Conteúdo Html", default="")
    evaluation = models.OneToOneField(Evaluation, on_delete=models.CASCADE)
    external_links = models.ManyToManyField(ExternalLink)