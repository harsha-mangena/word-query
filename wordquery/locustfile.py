from locust import HttpUser, task, between


class WordApiUser(HttpUser):
    wait_time = between(1, 2)  # Wait between 1 and 2 seconds between tasks

    @task
    def get_random_word(self):
        self.client.get("/word/random")

    @task
    def get_words_by_length(self):
        length = 5  # Example length, adjust as needed
        self.client.get(f"/word/length?len={length}")
