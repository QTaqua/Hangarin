import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

# Import Task, Category, and Priority models if Priority is a separate model
# If Priority is just a choices field, Django handles it as a string string
try:
    from hangarin.models import Task, Category, Priority
except ImportError:
    from hangarin.models import Task, Category
    Priority = None


class Command(BaseCommand):
    help = "Seeds database with fake tasks, categories, and priorities assigned to existing users."

    def add_arguments(self, parser):
        parser.add_argument(
            '--tasks-per-user',
            type=int,
            default=5,
            help='Number of fake tasks to generate per user'
        )

    def handle(self, *args, **options):
        fake = Faker()
        tasks_per_user = options['tasks_per_user']
        users = User.objects.all()

        if not users.exists():
            self.stdout.write(
                self.style.ERROR("No users found! Create a user first before seeding tasks.")
            )
            return

        self.stdout.write(self.style.WARNING("Seeding data..."))

        # 1. Handle Categories
        default_categories = ['Work', 'Personal', 'Shopping', 'Health', 'Finance']
        categories = []
        for cat_name in default_categories:
            cat_obj, _ = Category.objects.get_or_create(name=cat_name)
            categories.append(cat_obj)

        # 2. Handle Priorities (if Priority is a separate Model)
        priorities = []
        if Priority is not None:
            default_priorities = ['Low', 'Medium', 'High', 'Urgent']
            for prio_name in default_priorities:
                prio_obj, _ = Priority.objects.get_or_create(name=prio_name)
                priorities.append(prio_obj)

        # Inspect Task model fields dynamically
        model_fields = [f.name for f in Task._meta.get_fields()]

        total_tasks = 0
        status_choices = ['todo', 'in_progress', 'done', 'completed']
        string_priorities = ['low', 'medium', 'high', 'urgent']

        # 3. Generate Tasks
        for user in users:
            for _ in range(tasks_per_user):
                task_data = {}

                # User mapping
                if 'user' in model_fields:
                    task_data['user'] = user
                elif 'owner' in model_fields:
                    task_data['owner'] = user

                # Category mapping
                if 'category' in model_fields:
                    task_data['category'] = random.choice(categories)

                # Priority mapping (Model ForeignKey vs CharField Choices)
                if 'priority' in model_fields:
                    if priorities:
                        task_data['priority'] = random.choice(priorities)
                    else:
                        task_data['priority'] = random.choice(string_priorities)

                # Title mapping
                if 'title' in model_fields:
                    task_data['title'] = fake.sentence(nb_words=random.randint(3, 6)).rstrip('.')
                elif 'name' in model_fields:
                    task_data['name'] = fake.sentence(nb_words=random.randint(3, 6)).rstrip('.')

                # Description mapping
                if 'description' in model_fields:
                    task_data['description'] = fake.paragraph(nb_sentences=2)

                # Status / Completion mapping
                if 'status' in model_fields:
                    task_data['status'] = random.choice(status_choices)
                elif 'is_completed' in model_fields:
                    task_data['is_completed'] = fake.boolean(chance_of_getting_true=30)
                elif 'completed' in model_fields:
                    task_data['completed'] = fake.boolean(chance_of_getting_true=30)

                # Timezone-aware Deadline mapping
                naive_deadline = fake.future_datetime()
                aware_deadline = timezone.make_aware(naive_deadline, timezone.get_current_timezone())
                
                if 'deadline' in model_fields:
                    task_data['deadline'] = aware_deadline
                if 'due_date' in model_fields:
                    task_data['due_date'] = aware_deadline.date()

                Task.objects.create(**task_data)
                total_tasks += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {total_tasks} tasks across {users.count()} user(s)!")
        )