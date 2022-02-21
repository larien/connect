deliver:
	docker build . --tag larien/locations-api
	docker push larien/locations-api

deploy:
	kubectl apply -f deployment/
	kubectl rollout restart deployment locations-api

api: deliver deploy