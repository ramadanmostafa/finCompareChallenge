import re

from django.utils import timezone

from api.models import EmailData
from finCompareChallenge.celery import app


def get_email_from_list(lst):
    """
    iterate over every item of the input list and check if it's an email or not
    :param lst: list of stings
    :return: email address or empty str
    """
    for item in lst:
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", item):
            return item
    return ''


@app.task(bind=True)
def save_chunk(self, data):
    """
    initiate the save task for each row in the input data if it has a valid email
    :param self:
    :param data:
    :return:
    """
    for row in data:
        email = get_email_from_list(row)
        if email:
            save_record.delay(email, row)


@app.task(bind=True)
def save_record(self, email, data):
    # save the record to the database
    record, _ = EmailData.objects.get_or_create(email=email)
    record.data = data
    record.updated = timezone.now()
    record.save()
    return True
