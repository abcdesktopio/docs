# Create Kubernetes cluster on GCP to host demo platform

## Requirements

- a Google cloud account
- `gcloud` command line interface [gcloud cli](https://docs.cloud.google.com/sdk/docs/install-sdk/)

## Create a Kubernetes cluster 

This guide describes how to provision the infrastructure that hosts the `https://demo.gcp.abcdesktop.com` service on Google Cloud Platform.

### Prerequisites

- set up a [VPC](https://docs.cloud.google.com/vpc/docs?hl=fr)
- create 2 internal ranges, one for the subnet and one for the pods, before creating your cluster's subnet. See [this documentation](https://docs.cloud.google.com/vpc/docs/create-use-internal-ranges) for more information
- create a NAT gateway for the region you will deploy your cluster, check [Cloud NAT documentation](https://docs.cloud.google.com/nat/docs?hl=fr) for more inforation

### Configure gcloud cli

Authenticate to your GCP account using the following command.

```
gcloud auth login
```

Configure `gcloud` to set your GCP project as the active project by running the following command.

```
gcloud config set project <YOUR_PROJECT_ID>
```

### Deploying the cluster with gcloud cli

Deploy the Kubernetes cluster by running the following command.

```
gcloud beta container \
    --project \
"ino-abcdesktop-prd" clusters create "abcdesktop-demo-cluster" \
    --region \
"europe-west9" \
    --no-enable-basic-auth \
    --cluster-version \
"1.35.3-gke.1389000" \
    --release-channel \
"regular" \
    --machine-type \
"n4-standard-4" \
    --image-type \
"COS_CONTAINERD" \
    --disk-type \
"hyperdisk-balanced" \
    --disk-size \
"100" \
    --metadata \
disable-legacy-endpoints=true \
    --service-account \
"default" \
    --scopes \
"https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/trace.append" \
    --max-pods-per-node \
"110" \
    --num-nodes \
"6" \
    --logging=SYSTEM,WORKLOAD \
    --monitoring=SYSTEM,STORAGE,HPA,POD,DAEMONSET,DEPLOYMENT,STATEFULSET,CADVISOR,KUBELET,DCGM,JOBSET \
    --enable-private-nodes \
    --enable-ip-alias \
    --network \
"projects/ino-abcdesktop-prd/global/networks/vpc-demo-abcdesktop-network" \
    --subnetwork \
"projects/ino-abcdesktop-prd/regions/europe-west9/subnetworks/gke-abcdesktop-demo-cluster-subnet-a91bbd71" \
    --enable-intra-node-visibility \
    --default-max-pods-per-node \
"110" \
    --enable-autoscaling \
    --min-nodes \
"0" \
    --max-nodes \
"6" \
    --location-policy \
"BALANCED" \
    --enable-ip-access \
    --enable-authorized-networks-on-private-endpoint \
    --security-posture=standard \
    --workload-vulnerability-scanning=disabled \
    --enable-dataplane-v2 \
    --enable-dataplane-v2-metrics \
    --enable-dataplane-v2-flow-observability \
    --no-enable-google-cloud-access \
    --addons \
HorizontalPodAutoscaling,HttpLoadBalancing,NodeLocalDNS,GcePersistentDiskCsiDriver \
    --enable-autoupgrade \
    --enable-autorepair \
    --max-surge-upgrade \
1 \
    --max-unavailable-upgrade \
0 \
    --binauthz-evaluation-mode=DISABLED \
    --enable-managed-prometheus \
    --enable-shielded-nodes \
    --shielded-integrity-monitoring \
    --shielded-secure-boot \
    --node-locations \
"europe-west9-b","europe-west9-a","europe-west9-c"
```

!!!note
    The options shown above represent the recommended configuration, but you may adjust them to suit your environment. Ensure the following options remain enabled:
    - secure boot enabled
    - private nodes enabled 
    - dataplane V2 enabled

Finally, click the **Connect** button and paste the provided command into your terminal.