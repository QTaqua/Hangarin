from django.shortcuts import get_object_or_404, redirect, render
from .models import Priority, SubTask, Task


def task_board(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        subtask_id = request.POST.get("subtask_id")

        if task_id:
            task = get_object_or_404(Task, id=task_id)
            # Toggle or mark as completed; if main task is completed, complete all subtasks
            if task.status != "Completed":
                task.status = "Completed"
                task.save()
                task.subtasks.update(status="Completed")
            else:
                task.status = "Pending"
                task.save()

        elif subtask_id:
            subtask = get_object_or_404(SubTask, id=subtask_id)
            if subtask.status != "Completed":
                subtask.status = "Completed"
            else:
                subtask.status = "Pending"
            subtask.save()

        return redirect("task_board")

    priorities = Priority.objects.prefetch_related(
        "tasks__subtasks", "tasks__notes", "tasks__category"
    ).all()

    return render(request, "hangarin/task_board.html", {"priorities": priorities})