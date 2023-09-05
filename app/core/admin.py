from django.contrib import admin
from django.utils.html import format_html
from core.models import Sample
from django.contrib.admin import DateFieldListFilter
from django.contrib import messages
from datetime import datetime
from django.urls import path
from django.shortcuts import render, redirect


admin.site.register(Sample)
