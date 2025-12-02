# Poker Advisor API

## 1) Executive Summary

This project implements a fully containerized poker advisor service that is able to deliver real-time preflop recommendations using Monte Carlo simulations while also being able to tell players their equities and draws on subsequent streets. The system uses a FastAPI-based HTTP server where users are able to input their cards and other optional data such as position, stack, pot size, and action they might be facing. The service is then able to compute the expected equity through repeated random trials, find the opponent distribution, and then return a clear decision for the player based on the different equity thresholds based on the perceived ranges.

## 2) System Overview

### A. Course Concepts
- **Containerization (Docker)**: Deterministic runtime, reproducibility, ability to run locally
- **API/Webservices**: Creating a structured API design for ML/DS systems
- **Simulation Pipeline**: Creating a Monte Carlo Statistical model that is able to compute user equity
- **Cloud deployment (Azure)**: Allows app to be run virtually
- **Data modeling**: JSON based opponent hand range specification

### B. Architecture Overview

The architecture diagram for this project is found under the assets folder. The poker advisor uses a FastAPI server that is containerized using Docker. The server hosts an endpoint that accepts user poker hand data and optional game context. The server loads predefined opponent hand ranges from JSON files stored in the container. The service uses eval7 to compute the equities. Everything is packaged into a single Docker image and deployed to Azure Container Apps for public access, which provides a secure HTTPS endpoint. Users interact through a browser UI, which sends requests to the FastAPI backend.

![Poker Advisor Architecture](assets/arch_for_ds_project.png)

### C. Data/Models/Services

**Hand Range Data**
- Source: Custom JSON files stored in `/data/ranges*.json`
- Format: JSON
- Size: 5-10 KB each
- License: Self-developed for this project

**Simulation Engine (eval7)**
- Source: PyPI eval7 package
- Format: Python library
- License: MIT license
- Purpose: Fast hand evaluation for Monte Carlo trials

**FastAPI Application Service**
- Source: Local code in the `/app` directory
- Framework: FastAPI + Uvicorn
- Licenses: FastAPI (MIT), Uvicorn (BSD)

**Container Image**
- Base: Python 3.11+
- Artifacts: FastAPI server, simulation engine, JSON range files
- Image Size: ~230–260 MB
- License: Follows base Python + included packages

**Cloud Deployment (Optional)**
- Platform: Azure Container Apps
- Ingress: HTTPS
- Endpoint: Configurable via Azure

### API Endpoints

| Endpoint | Method | Description |
|---------|--------|--------------|
| `/simple-advise` | POST | Preflop advice engine |
| `/street-advise` | POST | Flop/turn/river analysis (equity + draws) |
| `/ranges` | GET | Returns available range names |
| `/health` | GET | Service readiness check |
| `/docs` | GET | FastAPI interactive Swagger UI |

## 3) How to Run (Local)

Before running the code, ensure Docker is open and running.

### Quick Start
```bash
docker build -t poker-advisor:latest .
docker run -p 8000:8000 poker-advisor:latest
```

You should see output indicating the server is running at `http://localhost:8000`. Copy this URL into your browser to use the service locally.

### Interactive Testing
Visit the Swagger UI for interactive API testing:
```
http://localhost:8000/docs
```

### One-Line Command
```bash
docker build -t poker-advisor . && docker run --rm -p 8000:8000 poker-advisor
```

## 4) Design Decisions

### Why This Concept?

**FastAPI over Flask or Django**
FastAPI was chosen for this project because it provides automatic request validation with Pydantic and has high performance. Flask requires more manual validation and is typically slower under concurrent workloads. Django was avoided because its large, monolithic structure was too complex for this lightweight service.

**Monte Carlo over Game Theory Solver (GTO)**
During development, a GTO solver was considered. However, implementing a true GTO solver would require heavy GPU hardware and immense amounts of training data. Monte Carlo simulation was selected instead because it provides a simulation-based approach that only relies on CPU computational workloads, requires no pre-training, and still produces reliable preflop equity estimates.

**Why JSON Files**
JSON files were chosen because they allow the system to remain simple and easy to modify. Users can directly edit JSON to customize ranges without touching code. A database was not used because it would introduce operational overhead and networking complexity.

### Tradeoffs

**Monte Carlo vs GTO Solver**
A true game theory service was attempted but proved unreliable for a simple, clean service. Monte Carlo Simulations were chosen instead because they're fast and run efficiently on CPU without GPU requirements.

**Preflop Only Scope**
Full hand modeling and complex multi-street advice were sacrificed to create a more reliable preflop engine that's easy to build and deploy. The service can provide equity and outs information but cannot provide postflop play advice.

**JSON Files vs Database**
JSON files lack version history and runtime editing capabilities, but they provide zero operational overhead, easier deployment, and very simple range customization.

**CPU Only vs GPU**
The service runs on CPU only, making it cost-friendly, portable, and usable on any laptop. GPU would allow more simulations and a more accurate bot but would not be accessible to many users.

## 5) Security and Privacy

This service does not handle any user personal information. Several measures ensure safe operation:

- **Input Validation**: The API uses Pydantic to validate all entries, rejecting improper submissions with appropriate error messages.
- **Privacy**: The service holds no user PII (Personally Identifiable Information) and maintains complete user privacy.
- **Error Handling**: The system avoids exposing internal stack traces or sensitive runtime details.
- **Isolation**: Docker isolation prevents dependency conflicts and provides a secure execution environment.

## 6) Operations (Logging, Metrics, Scaling & Limitations)

### Logging
FastAPI middleware tracks request metadata, simulation runtime, and error events. Logs exclude sensitive content and focus on operational health.

### Metrics
Azure Container Apps provides built-in metrics for CPU usage, memory consumption, request count, and container restarts. Future versions could add custom simulation-level metrics.

### Scaling
The stateless architecture enables easy horizontal scaling. Azure Container Apps can automatically scale replicas up or down based on CPU usage or request load.

### Operational Limitations
- Simulation is CPU-bound; large simulation counts increase response times
- No caching means identical requests recompute simulations, raising compute cost in high-traffic settings
- Single-container deployment means compute and API share CPU resources
- No rate-limiting by default (could be added via a proxy or FastAPI extension)
- JSON range files are loaded at runtime; malformed JSON causes startup failure

## 7) Results and Evaluation

### Example Output (UI)
![Poker Advisor UI](assets/poker_ui.png)

### Correctness Validation
- **Known Equities**: Verified results for common hands (e.g., AhKh vs JJ, AKs vs AQo) match published preflop equity tables within expected Monte Carlo variance (±0.5–1.0%)
- **Range Sampling**: Ensured JSON range distributions result in correctly weighted opponent hand samples
- **Repeatability**: For fixed RNG seeds, results remain consistent across runs

### API Validation
- **Input Validation**: Invalid card formatting returns 400 Bad Request; unknown range names produce safe error messages (no stack traces)
- **Health Check**: `/health` endpoint reliably returns service readiness
- **Load Testing**: Service remained stable under repeated bursts of 20–50 sequential requests

### Testing Suite

**A. Smoke Check Test**
Run the smoke test to verify basic functionality:
```bash
cd tests
python3.11 smoke_check.py
```
This should output AA equity with a green checkmark, signifying the service is running correctly.

**B. Deterministic Test**
```bash
cd tests
python3.11 -m pytest test_deterministic.py -q
```

**C. Range Tests**
```bash
cd tests
python3.11 -m pytest test_ranges.py -q
```
Should print "1 passed"

## 8) What's Next

Going forward, the main aspects that could be improved:

- **Postflop Advice Engine**: Implementation of comprehensive postflop strategy recommendations with position-adjusted strategies and equity realization modeling
- **GTO Solver Integration**: A true Game Theory Optimal (GTO) solver would be the ultimate goal, enabling:
  - Advice on all streets (flop, turn, river)
  - Adjustment to different opponent types and stack depths
  - More mathematically rigorous decision-making
- **Multi-Opponent Modeling**: Allow users to input multiple opponents and receive equity estimates based on full table dynamics
- **Advanced Features**:
  - Hand range editing UI
  - Solver integration for custom hand distributions
  - Performance optimization for faster simulations
  - Machine learning-based opponent modeling

## 9) License and Attribution

This project is licensed under the **MIT License**. See the `License.md` file for complete details.

### Dependencies and Attribution
- `eval7`: MIT Licensed - Fast poker hand evaluator
- `FastAPI`: MIT Licensed - Modern async web framework
- `Uvicorn`: BSD Licensed - ASGI server implementation
- `Pydantic`: MIT Licensed - Data validation library
- `Azure SDK`: Apache 2.0 Licensed - Cloud platform integration

### LINK References
  
  Github Repositories: https://github.com/whauf/Final_Poker_DS2026
  Public Cloud Link: poker-test-app.kindpebble-8f192353.northcentralus.azurecontainerapps.io

## 10) Cloud Deployment (Extra Credit)

### Prerequisites
Ensure you have the Azure CLI installed and are authenticated with your Azure subscription.

### Deployment Steps

1. **Log Into Azure**
   ```bash
   az login
   ```

2. **Create Resource Group**
   ```bash
   az group create --name poker-test-rg --location northcentralus
   ```

3. **Create Azure Container Registry (ACR)**
   ```bash
   az acr create \
     --resource-group poker-test-rg \
     --name pokerregistrytestwh \
     --sku Basic \
     --location northcentralus
   ```

4. **Log in to the Registry**
   ```bash
   az acr login --name pokerregistrytestwh
   ```

5. **Build, Tag, and Push Docker Image**
   ```bash
   docker build -t poker-advisor-test .
   docker tag poker-advisor-test pokerregistrytestwh.azurecr.io/poker-advisor:v2
   docker push pokerregistrytestwh.azurecr.io/poker-advisor:v2
   ```

6. **Register Required Azure Providers**
   ```bash
   az provider register --namespace Microsoft.App --wait
   az provider register --namespace Microsoft.OperationalInsights --wait
   ```

7. **Create Container App Environment**
   ```bash
   az containerapp env create \
     --name poker-test-env \
     --resource-group poker-test-rg \
     --location northcentralus
   ```

8. **Deploy the Application**
   ```bash
   az containerapp create \
     --name poker-test-app \
     --resource-group poker-test-rg \
     --environment poker-test-env \
     --image pokerregistrytestwh.azurecr.io/poker-advisor:v2 \
     --target-port 8000 \
     --ingress external \
     --registry-server pokerregistrytestwh.azurecr.io \
     --registry-identity system
   ```

9. **Get the Public URL**
   ```bash
   az containerapp show \
     --name poker-test-app \
     --resource-group poker-test-rg \
     --query properties.configuration.ingress.fqdn \
     --output tsv
   ```

### Observability and Monitoring

This project implements comprehensive observability with:
- **Uvicorn Logging**: All request traces and startup events logged to console
- **Docker Logs**: View with `docker logs <container_id>`
- **Pytest-based Testing**: Comprehensive test suite ensures code correctness
- **Azure Monitor Integration** (Optional): Enable through Azure Container Apps configuration

---

