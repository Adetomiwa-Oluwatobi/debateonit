"""from django.core.management.base import BaseCommand
from debate.models import Topic  # Update this import to match your app name
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")
django.setup()
class Command(BaseCommand):
    help = 'Loads debate topics from a .txt file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('this_house_debate_topics.txt')
  # adjust path if different
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"{file_path} not found"))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]

        for topic_text in topics:
            Topic.objects.get_or_create(title=topic_text)

        self.stdout.write(self.style.SUCCESS(f"{len(topics)} topics loaded successfully."))"""



"""from django.core.management.base import BaseCommand
from debate.models import *  # Change if your model is in another app
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "debateonit.settings")
django.setup()
class Command(BaseCommand):
    help = 'Load debate topics from a text file into the database'

    def handle(self, *args, **kwargs):
        # Adjust this path to where you moved the text file inside your project
        file_path = os.path.join('debateonit', 'this_house_debate_topics.txt')  # Relative to project root

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                topic_name = line.strip()
                if topic_name:
                    topic, created = Topic.objects.get_or_create(name=topic_name)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created topic: {topic_name}"))
                    else:
                        self.stdout.write(f"Topic already exists: {topic_name}")

        self.stdout.write(self.style.SUCCESS('Finished loading debate topics.'))
"""
import os
from django.core.management.base import BaseCommand
from ...models import Topic  # make sure 'debate' is your app name

class Command(BaseCommand):
    help = 'Load debate topics from a text file into the database'

    def handle(self, *args, **kwargs):
        # Adjust to the correct path of your .txt file (assumes it's next to manage.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'this_house_debate_topics.txt')

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                topic_title = line.strip()
                if topic_title:
                    topic, created = Topic.objects.get_or_create(title=topic_title)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created topic: {topic_title}"))
                    else:
                        self.stdout.write(f"Topic already exists: {topic_title}")

        self.stdout.write(self.style.SUCCESS('Finished loading topics.'))
