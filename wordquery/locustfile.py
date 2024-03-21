from locust import HttpUser, task, between


class WordApiUser(HttpUser):
    host = 'http://127.0.0.1:8000'
    wait_time = between(1, 2)

    @task
    def get_random_word(self):
        self.client.get("/word/random")

    @task
    def get_words_by_length(self):
        length = 5
        self.client.get(f"/word/length?len={length}")