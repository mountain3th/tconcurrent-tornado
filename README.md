### tconcurrent-tornado
---
Based on tornado's gen.coroutine decorator, everytime when we do some io operations(sleeping, readfile, socket..eta), we wrap it and yield a thread future.When the future is done,(is_done==True), the program continues.

#### Installation
---
`python setup.py install`

#### Usage
---
```python
import tconcurrent

# must use wraps here
@tconcurrent.ThreadPoolRunner.wraps()
def get(self):
    # when do some io operations, yield with a toncurrent's task
    yield tconcurrent.ThreadPoolRunner.create_task(func1)

    yield tconcurrent.ThreadPoolRunner.create_task(func1)

    self.finish()
```
See more details in examples/
