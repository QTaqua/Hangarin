import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from hangarin.models import Category, Note, Priority, SubTask, Task


class Command(BaseCommand):
    help = "Generate fake data for Task, Note, and SubTask models using Faker"

    def handle(self, *args, **options):
        fake = Faker()

        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        if not categories or not priorities:
            self.stdout.write(
                self.style.ERROR(
                    "Please populate Category and Priority data via Admin first!"
                )
            )
            return

        self.stdout.write("Seeding data...")

        # Create 15 Tasks
        statuses = ["Pending", "In Progress", "Completed"]
        tasks = []

        for _ in range(15):
            naive_datetime = fake.date_time_this_month()
            aware_deadline = timezone.make_aware(naive_datetime)

            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=aware_deadline,
                status=fake.random_element(elements=statuses),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )
            tasks.append(task)

        # Create SubTasks and Notes for the generated Tasks
        for task in tasks:
            # Create 1 to 3 SubTasks per Task
            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=statuses),
                )

            # Create 1 to 2 Notes per Task
            for _ in range(random.randint(1, 2)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded 15 Tasks, along with SubTasks and Notes!"
            )
        )