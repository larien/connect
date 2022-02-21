# Connect

Project 2 from [Cloud-Native Nanodegree](https://www.udacity.com/courses/cloud-native-application-architecture-nanodegree--nd064)

## Links

- Connect APP - [http://localhost:30000](http://localhost:30000)
- Connect API - [http://localhost:30001](http://localhost:30001)
- Persons API - [http://localhost:30002](http://localhost:30002)
- Locations API - [http://localhost:30003](http://localhost:30003)
## Prerequisites

- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
- `kind create cluster --name connect`
- `kubectl cluster-info --context kind-connect`
- `kubectl get node`
- `kubectl apply -f monolith/deployment/`

## Extracting the monolith

The first step is to understand how the current system is architected and identify clear context boundaries. There are three diagrams for that:

- API dependency graph, to analyze which object imports which object
[API dependency graph](./docs/api_dependency_graph.png)

- Layers dependency graph, to analyze how the layering communicates
[Layers dependency graph](./docs/layers_dependency_graph.png)

- Entities dependency graph, to understand how the entities are related among each other
[Entities dependency graph](./docs/entities_dependency_graph.png)

What is clear from the beginning is that Connection has two dependencies: Location and Person, while Location has one dependency: Person. It's possible to implement one service per entity.
The frontend calls two resources: Connection Data Resource and Persons Resource. Since these two entities will probably be separated in different services, we might need a proxy available for the frontend that will redirect the requests to the microservices.

A good candidate for the first refactoring would be Connection entity, since it only imports and isn't imported by anything. But there is no simple way for it to import Location and Person, so let's think of something else.

I see Person as the most isolated entity. Location needs a Person ID in order to be created, but this has no relation with Person model and it is received directly from the request. Therefore, we can start with a Person microservice and setup a proxy. The Person microservice will be an internal service that requires fast and reliable responses, so we can use gRPC to communicate. But we can use REST to start.

### Step 1: Person microservice structure

- person_service
  - person
    - model
    - schema
    - service
    - controller
  - routes
  - config

Methods:
    - Create
    - Retrive
    - Retrieve All

### Step 2: Create a proxy to redirect Person requests to Person microservice and the rest to the Monolith

This proxy will have the same address as the frontend is expecting and will communicate with Person service and the monolith via RESTful APIs. The monolith will have its address changed to have a smooth migration.

After that, it's clear that Location is coupled with Connection entity; we'll need to refactor and move Location logic in ConnectionService to Location methods before moving it to its own service.


### Step 3: Refactor and extract Location

- location_service
  - location
    - model
    - schema
    - service
    - controller
  - routes
  - config

Location is also an internal service and we can use gRPC for communication, but we can start with REST.

After that, we can finally get rid of the monolith and work on extracting Connection microservice. This service will require a RESTful API due to the communication with the frontend, but it'll also implement gRPC in the future to communicate with internal services.

### Step 4: Extract Connection

- connection_service
  - connection
    - model
    - schema
    - service
    - controller
  - routes
  - config

From that we have our microservices implemented and we can implement gRPC between them.

### Step 5: Implement gRPC communication in the internal services

After that, we need to evaluate the performance and possible caveats in the system.