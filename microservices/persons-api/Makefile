deliver:
	docker build . --tag larien/persons-api
	docker push larien/persons-api

deploy:
	kubectl apply -f deployment/
	kubectl rollout restart deployment persons-api