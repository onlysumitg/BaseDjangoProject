from typing import Any
from django.db.models import Model

from celery import app
from .models import UserActivity

@app.shared_task(name="log_user_activity" ,queue="useractivity")
def async_create_log_entry_logger(  user_id: Model = None, ip_address=None, user_agent=None, path=None, target: Model = None, message: str = '',
                            **kwargs):
    print(" async_create_log_entry_loggerasync_create_log_entry_logger ",message)
    # if create_log_entry.target:
    #     content_type = ContentType.objects.get_for_model(log_entry_data.target)
    #     object_id = log_entry_data.target.id

    if message:
        user_activity = UserActivity.objects.create(user_id=user_id,
                                     target=target,
                                     change_message=message,
                                     ip_address=ip_address,
                                     user_agent=user_agent,
                                     path=path
                                     )
        return True

    return False

    
