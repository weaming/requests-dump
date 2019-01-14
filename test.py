from requests_dump import Capturer
import requests

# 1.
capturer = Capturer()

# Or

# 1.
# disk_file = open("test.txt", "ab")
# capturer = Capturer(dump_file=disk_file, decode=False)

# 2.
response = requests.post("https://www.baidu.com", {"hi": "test"})
capturer.finish()  # write extra \n

# 3.
print(capturer.getall_req().decode())
