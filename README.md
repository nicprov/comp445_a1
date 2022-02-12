# comp445_a1

### Example commands
> python src/httpc.py get 'http://httpbin.org/get?course=networking&assignment=1'

> python src/httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'

> python src/httpc.py post -h Content-Type:application/json -d '{"Assignment": 1}' http://httpbin.org/post

> python src/httpc.py post -h Content-Type:application/json http://httpbin.org/post -f sample_input.json

> python src/httpc.py post -h Content-Type:application/json -d '{"Assignment": 1}' http://httpbin.org/post -o test.txt -v
