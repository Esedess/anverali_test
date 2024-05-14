up:
	sudo docker-compose -f docker-compose.yml up 

down:
	sudo docker-compose -f docker-compose.yml  down -v

build:
	sudo docker-compose -f docker-compose.yml up --build 

rebuild:
	sudo docker-compose -f docker-compose.yml up -d --build

rerun:
	sudo docker-compose -f docker-compose.yml  down -v
	sudo rm -r /www/db && sudo mkdir /www/db
	sudo rm -r /www/web && sudo mkdir /www/web
	sudo docker-compose -f docker-compose.yml up -d --build
	sudo docker-compose -f docker-compose.yml up

db:
	sudo docker-compose exec web flask create_db
	sudo docker-compose exec web flask seed_db

create_db:
	sudo docker-compose exec web flask create_db

drop_db:
	sudo docker-compose exec web flask drop_db

seed_db:
	sudo docker-compose exec web flask seed_db

rm_folders:
	sudo rm -r /www/db && sudo mkdir /www/db
	sudo rm -r /www/web && sudo mkdir /www/web