# rooms/models.py
from django.db import models

from debate.models import Topic



class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # You can use a ManyToManyField to associate multiple players with a room
    players = models.ManyToManyField('Player', related_name='rooms')

    def __str__(self):
        return f"Room: {self.id}"

class Player(models.Model):
    ROLE_CHOICES = [
        # British Parliamentary (8 speakers)
        ('PM', 'Prime Minister'),
        ('LO', 'Leader of Opposition'),
        ('DPM', 'Deputy Prime Minister'),
        ('DLO', 'Deputy Leader of Opposition'),
        ('MG', 'Member of Government'),
        ('MO', 'Member of Opposition'),
        ('GW', 'Government Whip'),
        ('OW', 'Opposition Whip'),
        
        # Asian Parliamentary (4 speakers)
        ('OG', 'Opening Government'),
        ('OO', 'Opening Opposition'),
        ('CG', 'Closing Government'),
        ('CO', 'Closing Opposition'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10)
    room = models.ForeignKey(Room, related_name='players_in_room', on_delete=models.CASCADE)
    # Scoring fields
    content_score = models.FloatField(default=0)
    style_score = models.FloatField(default=0)
    strategy_score = models.FloatField(default=0)
    poi_score = models.FloatField(default=0)
    total_score = models.FloatField(default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"
    
    def get_role_display(self):
        """Return the human-readable role name"""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)
    


from django.utils.text import slugify

class TutorialCategory(models.Model):
    """Category for organizing tutorials (e.g., Reading Materials, Videos)"""
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Tutorial Categories"
    
    def __str__(self):
        return self.name

class Tutorial(models.Model):
    """Individual tutorial resource (PDF, video, article)"""
    RESOURCE_TYPES = (
        ('pdf', 'PDF Document'),
        ('article', 'Web Article'),
        ('video', 'Video Tutorial'),
        ('guide', 'Guide'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE, related_name='tutorials')
    file = models.FileField(upload_to='tutorials/files/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    
    # For PDF/Article resources
    length = models.CharField(max_length=50, blank=True, help_text="E.g., '15 pages', '8 min read'")
    doc_image = models.ImageField(
        upload_to='doc_images/',   # folder where uploaded images go
        default='defaults/default_image.jpg',  # default image path inside MEDIA_ROOT
        blank=True,
        null=True
    )
    
    # For Video resources
    duration = models.CharField(max_length=10, blank=True, help_text="Video duration in format MM:SS")
    video_embed_url = models.URLField(blank=True, null=True, help_text="YouTube/Vimeo embed URL")
    
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order within category")
    
    class Meta:
        ordering = ['category', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)