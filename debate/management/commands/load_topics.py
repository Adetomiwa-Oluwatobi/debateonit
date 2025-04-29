from django.core.management.base import BaseCommand
from debate.models import Topic  # Update this import to match your app name
import os

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

        self.stdout.write(self.style.SUCCESS(f"{len(topics)} topics loaded successfully."))
