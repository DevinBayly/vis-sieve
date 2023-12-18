# Setup instructions
the main fast api instructions are here
https://fastapi.tiangolo.com/#installation

to be able to run this on your system in a container you might use this command to get a continuumio container for miniconda3
`docker run -it --rm -v $PWD:/place --network host continuumio/miniconda3`

then inside the container you would install fast api via the instructions above
`pip install fastapi uvicorn[standard]`

Then you would run the uvicorn start up command in the container after navigating to the `/place` folder
```
cd /place
uvicorn main:app --reload --port 8088
```

Then point your browser at `localhost:8088` 
