import csv

from io import BytesIO, TextIOWrapper

from django.conf import settings

from api.tasks import save_chunk


def save_data(csvfile):
    """
    initiate the save task for each chunk of the input csv file
    :param csvfile: an open csv file
    :return: None
    """
    for chunk in csvfile.chunks():
        reader = get_reader(chunk)
        save_chunk.delay(list(reader))

    csvfile.close()


def get_reader(buffer, delimiter=settings.CSV_DELIMITER):
    """
    Tries different encoding before choosing the right reader.
    :param delimiter:
    :param buffer: string buffer of the csv file
    :return:
    """
    reader = None
    encodings = ['utf-8', 'latin-1', 'windows-1250', 'windows-1252']
    for e in encodings:
        try:
            data = BytesIO(buffer)
            fh = TextIOWrapper(data, encoding=e)
            fh.readlines()
            data.seek(0)
            reader = csv.reader(fh, delimiter=delimiter, quotechar='"')
        except UnicodeDecodeError:
            pass  # error, try another encoding
        else:
            break  # encoding was successful
    return reader
