deliver:
	docker build . --tag larien/connections-api
	docker push larien/connections-api

deploy:
	kubectl apply -f deployment/
	kubectl rollout restart deployment connections-api

api: deliver deploy