from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Note, Priority, SubTask, Task


def task_board(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_task":
            title = request.POST.get("title")
            description = request.POST.get("description")
            deadline = request.POST.get("deadline")
            priority_id = request.POST.get("priority")
            category_id = request.POST.get("category")

            if title and priority_id and category_id and deadline:
                priority = get_object_or_404(Priority, id=priority_id)
                category = get_object_or_404(Category, id=category_id)
                Task.objects.create(
                    title=title,
                    description=description,
                    deadline=deadline,
                    priority=priority,
                    category=category,
                )

        elif action == "edit_task":
            task_id = request.POST.get("task_id")
            if task_id:
                task = get_object_or_404(Task, id=task_id)
                task.title = request.POST.get("title", task.title)
                task.description = request.POST.get("description", task.description)
                deadline = request.POST.get("deadline")
                if deadline:
                    task.deadline = deadline
                priority_id = request.POST.get("priority")
                if priority_id:
                    task.priority = get_object_or_404(Priority, id=priority_id)
                category_id = request.POST.get("category")
                if category_id:
                    task.category = get_object_or_404(Category, id=category_id)
                task.save()

                # Add new Subtask if provided
                new_subtask_title = request.POST.get("new_subtask_title")
                if new_subtask_title and new_subtask_title.strip():
                    SubTask.objects.create(
                        parent_task=task,
                        title=new_subtask_title.strip(),
                        status="Pending",
                    )

                # Add new Note if provided
                new_note_content = request.POST.get("new_note_content")
                if new_note_content and new_note_content.strip():
                    Note.objects.create(
                        task=task,
                        content=new_note_content.strip(),
                    )

        elif action == "delete_subtask":
            subtask_id = request.POST.get("subtask_id")
            if subtask_id:
                subtask = get_object_or_404(SubTask, id=subtask_id)
                subtask.delete()

        elif action == "delete_note":
            note_id = request.POST.get("note_id")
            if note_id:
                note = get_object_or_404(Note, id=note_id)
                note.delete()

        elif action == "delete_task":
            task_id = request.POST.get("task_id")
            if task_id:
                task = get_object_or_404(Task, id=task_id)
                task.delete()

        elif action == "toggle_task":
            task_id = request.POST.get("task_id")
            if task_id:
                task = get_object_or_404(Task, id=task_id)
                if task.status != "Completed":
                    task.status = "Completed"
                    task.save()
                    task.subtasks.update(status="Completed")
                else:
                    task.status = "Pending"
                    task.save()

        elif action == "toggle_subtask":
            subtask_id = request.POST.get("subtask_id")
            if subtask_id:
                subtask = get_object_or_404(SubTask, id=subtask_id)
                subtask.status = (
                    "Completed" if subtask.status != "Completed" else "Pending"
                )
                subtask.save()

        return redirect("task_board")

    priorities = Priority.objects.prefetch_related(
        "tasks__subtasks", "tasks__notes", "tasks__category"
    ).all()
    categories = Category.objects.all()

    return render(
        request,
        "hangarin/task_board.html",
        {"priorities": priorities, "categories": categories},
    )