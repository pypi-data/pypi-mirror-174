# dasker
monadic dask

example:
    dasker '{}' python -c "import dasker; print(dasker.get_client().submit(lambda: 'hello, world!').result())"

equivalent example, because it's a monad:
    dasker '{}' dasker '{}' python -c "import dasker; print(dasker.get_client().submit(lambda: 'hello, world!').result())"

if dasker wasn't used to start dask, a default client is used. example:
    python -c "import dasker; print(dasker.get_client().submit(lambda: 'hello, world!').result())"

if you want to override the contextual dask, use --force-new. example:
    dasker '{"processes": false}' dasker --force-new '{"processes": true, "nthreads": 1, "n_workers": 1}' command ...

