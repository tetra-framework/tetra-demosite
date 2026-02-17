from tetra import public
from tetra.components.reactive import ReactiveComponent
from demo.models import ToDo


class TodoItem(ReactiveComponent):
    title = public("")
    done = public(False)
    model_version = public(0)
    todo: ToDo

    def load(self, todo: ToDo, *args, **kwargs):
        self.todo = todo
        self.title = todo.title
        self.done = todo.done
        self.model_version = todo.model_version

    def get_subscription(self) -> str:
        return self.todo.get_tetra_instance_channel()

    @public.watch("title", "done")
    @public.debounce(200)
    def save(self, value, old_value, attr):
        self.todo.title = self.title
        self.todo.done = self.done
        self.todo.save()
        # Update local version to match saved version
        self.model_version = self.todo.model_version

    @public(update=False)
    def delete_item(self):
        # Delete the todo - ReactiveModel will send WebSocket notification
        self.todo.delete()
        self.client._removeComponent()
