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
  Edit the following 5 paths in `cradle/settings.py` to the paths on your machine.
  - OPENAI_API_KEY
  - RAW_REVIEW_DIR
  - FILTER_REVIEW_DIR
  - GUIDE_PATH
  - STOREID2STORENAME_MAP_PATH

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
import requests

# assuming your IP is: XXX.XXX.XXX.XXX
url = "XXX.XXX.XXX.XXX/petlover/callback"

data_dict = {
    "txt": "%petfriendly%  faherty",
}

response = requests.post(url, data=data_dict)

# Check the response status and handle accordingly.
if response.status_code == 200:
    print("POST request successful!")
    response_data = response.json()
    print(response_data)
else:
    print(f"Failed to make a POST request. Status code: {response.status_code}")

```
