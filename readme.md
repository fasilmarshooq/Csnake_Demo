This is a small api project to create a vector search in dontet using [CSnake](https://github.com/tonybaloney/CSnakes) and [ChromaDb](https://docs.trychroma.com/docs/overview/introduction)

The earlier Interop providers like Python.net take interop process approach but the Csnake takes code gen approach.

Basically we have exposted two methods from [chroma_db.py](./python/chroma_db.py) Add and Search , CSnake just do code gen and we can access them just like we access our C# methods.

performance is not that bad, i have attached some stress test results [here](./load_test/stress_test_report.html)

