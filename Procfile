release: python manage.py migrate 
web: gunicorn : Blog_app.wsgi --log-file -
web: gunicorn Blog_app.config.settings.wsgi

web: gunicorn Blog_app.wsgi:application --log-file -
