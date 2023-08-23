from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/api/v1/auth/users")
        self.client.get("/api/v1/auth/get?user_id=2")