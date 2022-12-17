from locust import HttpUser, task


class PerformanceTests(HttpUser):

    @task
    def check_prime(self):
        self.client.get(url='Prime/13')

    @task
    def check_invert(self):
        in_file = open('Lena.jpg', 'rb')
        data = in_file.read()
        self.client.post(url="picture/invert", files={'file': data})

    @task
    def check_auth(self):
        self.client.get(url='Auth', auth=("admin", "admin"))
