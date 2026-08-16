# Cloud Providers

## Tier 1: The Managed Abstraction

These platforms abstract away the infrastructure, allowing you to interact directly with the model via an API.  

[Novita](https://novita.ai/): Operates a managed AI cloud providing over 200 pre-integrated serverless model APIs (text, image, audio) billed by the token. It requires zero infrastructure provisioning for its API endpoints.

## Tier 2: Self-Hosted Production

[RunPod](https://runpod.io/gsc): Provides rented GPU containers and serverless endpoints. You maintain full control over the Docker environment and the specific inference architecture deployed within the pod.

[Vast.ai](https://cloud.vast.ai/): A decentralized marketplace for renting raw GPU instances. You receive SSH and Docker access, assuming full responsibility for environment configuration, model deployment, and fault tolerance.

[JarvisLabs.ai](https://jarvislabs.ai/): Provisions dedicated GPU virtual machines pre-loaded with ML frameworks (via SSH or Jupyter). You manage the deployment pipeline and the underlying inference engine.

[Modal](https://www.modal.com/): Functions as a highly abstracted Tier 2 provider. While it manages serverless scaling, developers must write the Python code that defines the container dependencies, provisions the hardware, and executes the specific inference engine logic.

## Tier 3: Bare-metal Access (Deep Engineering Required)

[Latitude.sh](https://latitude.sh/): A pure bare-metal cloud provider. You rent the physical servers, granting complete control over the hypervisor, storage arrays, and high-bandwidth networking required for custom inference stacks.

[PRIME Intellect](https://app.primeintellect.ai/): A decentralized high-performance computing platform engineered for large-scale operations. It facilitates multi-node cluster orchestration (e.g., Slurm, Kubernetes), distributed training, and massive inference workloads across vast global GPU networks.

[Novita](https://novita.ai/): Beyond its APIs, Novita provides enterprise-grade bare-metal GPU clusters (e.g., interconnected H100s via NVLink and RDMA) designed for continuous, high-throughput enterprise batching.  

### Vertical Stack

[Modular](https://www.modular.com/) occupies a unique position: **it spans all three tiers**, but its core identity and greatest value proposition sit firmly in Tier 3.

- Tier 1: Hosted Model API Endpoints
- Tier 2: MAX Container
- Tier 3: The Mojo programming language
