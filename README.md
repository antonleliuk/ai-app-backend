poetry config virtualenvs.in-project true
poetry install

https://python-poetry.org/docs/basic-usage/

poetry shell
poentry run python /src/app/start.py

sudo ln -s /home/pi/ai-app/scripts/ai-service.service /etc/systemd/system/ai-service.service

# Take a picture
fswebcam -S 1 -v test.jpg