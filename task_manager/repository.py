class TaskRepository:
    def __init__(self, storage):
        self.storage = storage
        self._next_id = 1

    def save(self, task):
        task.id = self._next_id
        self._next_id += 1
        self.storage.add(task.id, task)
        return task

    def find_by_id(self, id):
        return self.storage.get(id)

    def find_all(self):
        return self.storage.get_all()

    def delete(self, id):
        self.storage.delete(id)