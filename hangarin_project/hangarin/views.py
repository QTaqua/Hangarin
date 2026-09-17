from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task, Priority, Category, SubTask, Note


# --- Signup / Registration View ---
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log user in after registration
            return redirect('task_board')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# --- Main Task Board View (Protected) ---
@login_required
def task_board(request):
    if request.method == "POST":
        action = request.POST.get('action')

        # AJAX: Add Subtask
        if action == 'ajax_add_subtask':
            task_id = request.POST.get('task_id')
            title = request.POST.get('title', '').strip()
            task = get_object_or_404(Task, id=task_id, user=request.user)
            subtask = SubTask.objects.create(parent_task=task, title=title, status='Pending')
            return JsonResponse({'status': 'success', 'id': subtask.id, 'title': subtask.title})

        # AJAX: Add Note
        elif action == 'ajax_add_note':
            task_id = request.POST.get('task_id')
            content = request.POST.get('content', '').strip()
            task = get_object_or_404(Task, id=task_id, user=request.user)
            note = Note.objects.create(task=task, content=content)
            return JsonResponse({'status': 'success', 'id': note.id, 'content': note.content})

        # Form Submit: Create Task
        elif action == 'create_task':
            title = request.POST.get('title')
            description = request.POST.get('description')
            deadline = request.POST.get('deadline')
            priority_id = request.POST.get('priority')
            category_id = request.POST.get('category')

            if title and priority_id and category_id and deadline:
                priority = get_object_or_404(Priority, id=priority_id)
                category = get_object_or_404(Category, id=category_id)
                Task.objects.create(
                    user=request.user,  # Attach current logged in user
                    title=title,
                    description=description,
                    deadline=deadline,
                    priority=priority,
                    category=category
                )

        # Form Submit: Edit Task
        elif action == 'edit_task':
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task.title = request.POST.get('title', task.title)
            task.description = request.POST.get('description', task.description)
            if request.POST.get('deadline'):
                task.deadline = request.POST.get('deadline')
            if request.POST.get('priority'):
                task.priority = get_object_or_404(Priority, id=request.POST.get('priority'))
            if request.POST.get('category'):
                task.category = get_object_or_404(Category, id=request.POST.get('category'))
            task.save()

        # Form Submit: Delete Task
        elif action == 'delete_task':
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task.delete()

        # Form Submit: Toggle Task Status
        elif action == 'toggle_task':
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id, user=request.user)
            if task.status != 'Completed':
                task.status = 'Completed'
                task.save()
                task.subtasks.update(status='Completed')
            else:
                task.status = 'Pending'
                task.save()

        # Form Submit: Toggle Subtask Status
        elif action == 'toggle_subtask':
            subtask_id = request.POST.get('subtask_id')
            subtask = get_object_or_404(SubTask, id=subtask_id, parent_task__user=request.user)
            subtask.status = 'Pending' if subtask.status == 'Completed' else 'Completed'
            subtask.save()

        # Form Submit: Delete Subtask
        elif action == 'delete_subtask':
            subtask_id = request.POST.get('subtask_id_del')
            subtask = get_object_or_404(SubTask, id=subtask_id, parent_task__user=request.user)
            subtask.delete()

        # Form Submit: Delete Note
        elif action == 'delete_note':
            note_id = request.POST.get('note_id_del')
            note = get_object_or_404(Note, id=note_id, task__user=request.user)
            note.delete()

        return redirect('task_board')

    # Fetch priorities and only include tasks belonging to the current user
    priorities = Priority.objects.prefetch_related(
        models.Prefetch(
            'tasks',
            queryset=Task.objects.filter(user=request.user).prefetch_related('subtasks', 'notes', 'category')
        )
    ).all()
    categories = Category.objects.all()

    return render(request, 'hangarin/task_board.html', {
        'priorities': priorities,
        'categories': categories
    })