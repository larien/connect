deliver-api:
	docker build . --tag larien/nd064-udaconnect-api
	docker push larien/nd064-udaconnect-api

deploy-api:
	cd ../../ && kubectl apply -f deployment/
	kubectl rollout restart deployment udaconnect-api

api: deliver-api deploy-api