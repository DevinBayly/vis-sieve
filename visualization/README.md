# Setup instructions

## Setup Docker container
First things first, run this docker command

On linux:
`docker run -it --rm -v $PWD:/place --network host continuumio/miniconda3`

On mac os:
1. Open Docker app
2. Open Terminal, navigate to this `vis-seive/visualization` directory
3. Run Carolina's instructions below
```
    created $(pwd)/place directory beforehand
    and then ran docker run -it --rm --mount type=bind,source="$(pwd)",target=/place -p 8080:8080 continuumio/miniconda3
```
This makes it possible to run fast api install instructions without messing with your other python programs (outside the container). 

## Install FastAPI within docker container
the main fast api instructions are here
https://fastapi.tiangolo.com/#installation

then inside the container you would install fast api via the instructions above
`pip install fastapi uvicorn[standard]`

## Run uvicorn
Then you would run the uvicorn start up command in the container after navigating to the `/place` folder
```
cd /place
uvicorn main:app --reload --port 8088
```

Then point your browser at `localhost:8088` 

## Exit

On mac os:
^C then ^D (^ = ctrl)
