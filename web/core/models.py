from django.db import models

class AlertSettings(models.Model):
    ALERT_TYPES = [
        ('success', 'Succès (Vert)'),
        ('info', 'Info (Bleu)'),
        ('warning', 'Avertissement (Jaune)'),
        ('danger', 'Danger (Rouge)'),
        ('primary', 'Primaire (Bleu Foncé)'),
    ]

    METRIC_CHOICES = [
        ('wind_speed', 'Vitesse du Vent'),
        ('temperature', 'Température'),
        ('humidity', 'Humidité'),
        ('pressure', 'Pression'),
        ('sys_update', 'Mise à jour Système'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom de l'alerte")
    metric = models.CharField(max_length=50, choices=METRIC_CHOICES, verbose_name="Métrique surveillée")
    min_value = models.FloatField(null=True, blank=True, verbose_name="Valeur Min (Exclusif)")
    max_value = models.FloatField(null=True, blank=True, verbose_name="Valeur Max (Exclusif)")
    message = models.TextField(verbose_name="Message à afficher")
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES, default='info', verbose_name="Type d'alerte")
    icon = models.CharField(max_length=50, default='bi-info-circle-fill', verbose_name="Classe Icône Bootstrap")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return self.name


class SensorFallback(models.Model):
    """
    Singleton model to store fallback values when InfluxDB is down or empty.
    """
    vent_vitesse = models.FloatField(verbose_name="Vitesse Vent (km/h)")
    vent_dir = models.CharField(max_length=10, verbose_name="Direction Vent (ex: N, S, NW)")
    vent_angle = models.FloatField(verbose_name="Angle Vent (degrés)")
    temperature = models.FloatField(verbose_name="Température (°C)")
    humidite = models.FloatField(verbose_name="Humidité (%)")
    pression = models.FloatField(verbose_name="Pression (hPa)")
    luminosite = models.FloatField(verbose_name="Luminosité (Lux)")

    def __str__(self):
        return "Valeurs par défaut (Fallback)"

    def save(self, *args, **kwargs):
        if not self.pk and SensorFallback.objects.exists():
             # If you want to ensure only one exists, you can delete old one or update it.
             # Ideally we just prevent creating new ones in admin, but for now strict singleton:
             return SensorFallback.objects.first().save(*args, **kwargs) # Prevent multiple? Or just overwrite?
             # Let's keep it simple: allow user to manage, but Views will pick '.first()'
        super(SensorFallback, self).save(*args, **kwargs)
