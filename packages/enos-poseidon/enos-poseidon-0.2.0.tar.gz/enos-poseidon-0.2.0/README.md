## Project description
Athena is the core SDK for requesting the EnOS API

### Example

#### 1.1 Query

```python
from poseidon.poseidon import poseidon

appkey = 'xxxxx-xxxx-xxxx-xxxx-xxxxxxxx'
appsecret = 'xxxxx-xxxx-xxxx-xxxx-xxxxxx'

url = 'http://{apim-url}/someservice/v1/tyy?sid=28654780'

req = poseidon.urlopen(appkey, appsecret, url)
print(req)
```
#### 1.2 Header

```python
from poseidon.poseidon import poseidon

appkey = 'xxxxx-xxxx-xxxx-xxxx-xxxxxxxx'
appsecret = 'xxxxx-xxxx-xxxx-xxxx-xxxxxx'

url = 'http://{apim-url}/someservice/v1/tyy?sid=28654780'

header = {}

req = poseidon.urlopen(appkey, appsecret, url, None, header)
print(req)

```

#### 1.3 Body

```python
from poseidon.poseidon import poseidon

appkey = 'xxxxx-xxxx-xxxx-xxxx-xxxxxxxx'
appsecret = 'xxxxx-xxxx-xxxx-xxxx-xxxxxx'

url = 'http://{apim-url}/someservice/v1/tyy?sid=28654780'

data = {"username": "11111", "password": "11111"}

req = poseidon.urlopen(appkey, appsecret, url, data)
print(req)

```