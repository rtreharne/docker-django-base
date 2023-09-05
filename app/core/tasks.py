from __future__ import absolute_import, unicode_literals
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
import time
import re

logger = get_task_logger(__name__)

