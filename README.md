# cradle-django

## Data
Download from https://drive.google.com/drive/folders/1K6-OSrJXWz5ekSmmepAuEYi5iAVy24wa
## Settings

- Step-1:  
Enter a docker container using the following docker image:  
    `nvcr.io/nvidia/pytorch:21.03-py3`
  ```
  # example command to start a docker container
  # named "pet"
  # mapping port "200:200" (local machine : inside container)
  # mapping volumn "/:/TOP" (local machine : inside container)
  # using image(nvcr.io/nvidia/pytorch:21.03-py3)
  
  docker run -d -it --name pet -p 200:200 -v /:/TOP nvcr.io/nvidia/pytorch:21.03-py3
  ```

  ```
  # example command to enter the container
  docker exec -it pet bash
  ```
- Step-2:  
Go to your working directory and clone this repo.  
Go into the repo.
- Step-3:
  
  ```
  pip install -r requirments.txt
  ```
- Step-4:
  Get submodules.
  ```
  git submodule update --init --recursive
  ```

- Step-5:
  Start the service.
  ```
  python manage.py migrate
  # assuming you use port 200
  python manage.py runserver 0.0.0.0:200
  ```

