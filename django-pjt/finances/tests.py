from django.test import TestCase

# Create your tests here.

from datetime import datetime, timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
print('어제날짜는?', yesterday)