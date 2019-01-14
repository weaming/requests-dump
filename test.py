from requests_dump import Capturer
import requests

# 1. init and patch HTTPConnection.send
capturer = Capturer()

# Or

# 1.
# disk_file = open("test.txt", "ab")
# capturer = Capturer(dump_file=disk_file, decode=False)

# 2.
response = requests.post("https://www.baidu.com", {"hi": "test"})
capturer.finish()  # write extra \n to dump_file after finish one request

# 3.
print(capturer.getall().decode())

# 4.
capturer.unpatch()
