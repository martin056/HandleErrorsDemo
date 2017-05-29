# HandleErrorsDemo
Simple django project demo for Handle Errors From Third Party Apps blog post.

### Run it:
0. Create virtualenv
1. ```$ pip install requirements.txt```
2. ```$ python3 manage.py runserver```
3. **In other tab: ** ```$ celery -A handle_errors_demo worker -l info```
4. Navigate to `localhost:8000/demo`