# cradle-django

## Data
Download from https://drive.google.com/drive/folders/1K6-OSrJXWz5ekSmmepAuEYi5iAVy24wa
## Settings

- Step-1:  
Enter a docker container using the following docker image:  
    `nvcr.io/nvidia/pytorch:21.03-py3`
  ```
  # example command to start a docker container named "my_container"
  # mapping port "200:200" (local machine : inside container)
  # mapping volumn "{your_project_folder_path}:/TOP" (local machine : inside container)
  # using image(nvcr.io/nvidia/pytorch:21.03-py3)
  
  docker run -d -it --name my_container -p 200:200 -v /my_project_folder_path:/TOP nvcr.io/nvidia/pytorch:21.03-py3
  ```

  ```
  # example command to enter the container
  docker exec -it my_container bash
  ```
- Step-2:  
Go to your working directory and clone this repo.  
Go into the repo.

- Step-3: 
  
  Edit the following information in `cradle/settings.py` to the paths on your machine.
  - OPENAI_API_KEY
  - GOOGLE_REVIEW_DIR
  - PUBLIC_IP

- Step-4:
  
  ```
  pip install -r requirments.txt
  ```
- Step-5:
  Get submodules.
  ```
  git submodule update --init --recursive
  ```

- Step-6:
  Start the service.

  ```
  python manage.py migrate
  # assuming you use port 200
  python manage.py runserver 0.0.0.0:200
  ```

## POST example (python)
```
import io
import requests

url = "XXX.XXX.XXX.XXX/petlover/callback"

data_dict = {
    "txt": "%petfriendly%  peak design",
}
def get_stream():
    s = requests.Session()

    #with s.post(url, json=data_dict, stream=True, data=io.BytesIO(b'many many bytes')) as resp:
    with s.post(url, json=data_dict, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                print(line)

get_stream()
```

## POST example (bash)
```
curl -X POST XXX.XXX.XXX.XXX/petlover/callback \
--header "Content-Type: application/json" \
--data '{"txt": "%petfriendly%  peak design"}'
```
