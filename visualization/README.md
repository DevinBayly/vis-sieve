# Setup instructions
First things first, run this docker command

linux `docker run -it --rm -v $PWD:/place --network host continuumio/miniconda3`
mac os `docker run -it --rm -v ${pwd}:/place continuumio/miniconda3`
This makes it possible to run fast api install instructions without messing with your other python programs (outside the container). 


the main fast api instructions are here
https://fastapi.tiangolo.com/#installation

then inside the container you would install fast api via the instructions above
`pip install fastapi uvicorn[standard]`

Then you would run the uvicorn start up command in the container after navigating to the `/place` folder
```
cd /place
uvicorn main:app --reload --port 8088
```

Then point your browser at `localhost:8088` 
