from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.gis.db import models as geomodels

User = get_user_model()


# Модель определенной точки на карте
class Point(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='points',
        verbose_name='Создатель точки'
    )

    name = models.CharField(
        max_length=250,
        verbose_name='Название точки',
    )

    coordinates = geomodels.PointField(
        srid=4326,
        verbose_name='Координаты точки'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания точки'
    )

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# Модель сообщения, привязанного к точке
# К одной точке может быть привязано много сообщений
class Message(models.Model):
    text = models.TextField(
        max_length=800,
        verbose_name='Текст сообщения'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        verbose_name='Автор сообщения'
    )

    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='К какой точке относится'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение от {self.user} для {self.point.name}"
