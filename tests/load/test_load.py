from locust import HttpUser, task


class HTTPUser(HttpUser):
    host = "http://127.0.0.1:8000"  # Хост, на который отправляются запросы

    @task
    def get_index(self):
        self.client.get("/")

    @task(3)
    def get_style(self):
        self.client.get("/style.css")
