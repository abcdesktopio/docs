---
render_macros: true
---

# keysgenerator

Keygenerator is a helper Docker image that provides tools to generate SSL public/private key pairs and store them in Kubernetes secrets when they don't already exist. This functionality is used to create self-signed certificates for internal communication between different services or pods within abcdesktop.

## Usage

In the Helm chart, the `keysgenerator` image is utilized by `jobs` to generate keys by executing the following command:

``` yaml
openssl genrsa -out abcdesktop_jwt_desktop_payload_private_key.pem {{ .Values.keysgenerator.jwtdesktoppayloadkeylength }} && \
openssl rsa -in abcdesktop_jwt_desktop_payload_private_key.pem -outform PEM -pubout -out  _abcdesktop_jwt_desktop_payload_public_key.pem && \
openssl rsa -pubin -in _abcdesktop_jwt_desktop_payload_public_key.pem -RSAPublicKey_out -out abcdesktop_jwt_desktop_payload_public_key.pem && \
if ! kubectl get secret abcdesktopjwtdesktoppayload --namespace={{ .Release.Namespace }} >/dev/null 2>&1;
then
    if ! kubectl create secret generic abcdesktopjwtdesktoppayload --from-file=abcdesktop_jwt_desktop_payload_private_key.pem --from-file=abcdesktop_jwt_desktop_payload_public_key.pem --namespace={{ .Release.Namespace }};
    then
        echo "Failed to create secret"
        exit 1
    fi
else
    echo "Secret already exists"
    exit 0
fi
```

The following jobs are executed once during Helm chart installation or upgrade. If the target secret already exists, it will not be recreated. Otherwise, it will be created with newly generated public/private key pairs:

- generate-jwtdesktoppayload-keys
- generate-jwtdesktopsigning-keys
- generate-jwtusersigning-keys
- generate-mongod-keyfile
