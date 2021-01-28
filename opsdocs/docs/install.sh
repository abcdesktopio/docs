#!/bin/sh

#
# This file is from Istio https://raw.githubusercontent.com/istio/istio/master/release/downloadIstioCandidate.sh
# Copyright Istio Authors
#
# Change for abcdesktopio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This file will be fetched as: curl -L https://git.io/getLatestIstio | sh -
# so it should be pure bourne shell, not bash (and not reference other scripts)
#
# The script fetches the latest Istio release candidate and untars it.
# You can pass variables on the command line to download a specific version
# or to override the processor architecture. For example, to download
# Istio 1.6.8 for the x86_64 architecture,
# run curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.6.8 TARGET_ARCH=x86_64 sh -.


# Determines the operating system.
OS="$(uname)"
if [ "x${OS}" = "xDarwin" ] ; then
  OSEXT="osx"
else
  OSEXT="linux"
fi

LOCAL_ARCH=$(uname -m)
if [ "${TARGET_ARCH}" ]; then
    LOCAL_ARCH=${TARGET_ARCH}
fi

case "${LOCAL_ARCH}" in 
  x86_64)
    OIO_ARCH=amd64
    ;;
  armv8*)
    OIO_ARCH=arm64
    ;;
  aarch64*)
    OIO_ARCH=arm64
    ;;
  armv*)
    OIO_ARCH=armv7
    ;;
  amd64|arm64)
    OIO_ARCH=${LOCAL_ARCH}
    ;;
  *)
    echo "This system's architecture, ${LOCAL_ARCH}, isn't supported"
    exit 1
    ;;
esac

echo "This system's architecture is ${OIO_ARCH}"

# Check if kubectl command is supported
# run command kubectl version
KUBE_VERSION=$(kubectl version)
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] 
then 
	echo "'kubectl version' command was successful"
else
	echo "'kubectl version' failed"
	echo "Please install kubectl command first"
	exit $?
fi



# Check if kubectl command is supported
# run command kubectl version
OPENSSL_VERSION=$(openssl version)
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] 
then
        echo "'openssl version' command was successful"
else
        echo "'openssl version' failed"
        echo "Please install openssl command first"
        exit $?
fi



# First create the abcdesktop namespace
kubectl create namespace abcdesktop
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] 
then
        echo "'kubectl create namespace abcdesktop' command was successful"
fi


# RSA keys
# build rsa kay pairs for jwt payload 
# 1024 bits is a smallest value, change here if need but use more than 1024
if [ ! -f abcdesktop_jwt_desktop_payload_private_key.pem ]
then
	openssl genrsa -out abcdesktop_jwt_desktop_payload_private_key.pem 1024
	openssl rsa    -in  abcdesktop_jwt_desktop_payload_private_key.pem -outform PEM -pubout -out  _abcdesktop_jwt_desktop_payload_public_key.pem
	openssl rsa    -pubin -in _abcdesktop_jwt_desktop_payload_public_key.pem -RSAPublicKey_out -out abcdesktop_jwt_desktop_payload_public_key.pem
fi

# build rsa kay pairs for the desktop jwt signing
if [ ! -f abcdesktop_jwt_desktop_signing_private_key.pem ]
then
	openssl genrsa -out abcdesktop_jwt_desktop_signing_private_key.pem 1024
	openssl rsa    -in  abcdesktop_jwt_desktop_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_desktop_signing_public_key.pem
fi

# build rsa kay pairs for the user jwt signing 
if [ ! -f abcdesktop/io_jwt_user_signing_private_key.pem ]
then
	openssl genrsa -out abcdesktop_jwt_user_signing_private_key.pem 1024
	openssl rsa    -in  abcdesktop_jwt_user_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_user_signing_public_key.pem
fi

# Import RSA Keys as Kubernetes secrets 
kubectl create secret generic abcdesktopjwtdesktoppayload --from-file=abcdesktop_jwt_desktop_payload_private_key.pem --from-file=abcdesktop_jwt_desktop_payload_public_key.pem --namespace=abcdesktop
kubectl create secret generic abcdesktopjwtdesktopsigning --from-file=abcdesktop_jwt_desktop_signing_private_key.pem --from-file=abcdesktop_jwt_desktop_signing_public_key.pem --namespace=abcdesktop
kubectl create secret generic abcdesktopjwtusersigning    --from-file=abcdesktop_jwt_user_signing_private_key.pem    --from-file=abcdesktop_jwt_user_signing_public_key.pem    --namespace=abcdesktop

# create abcdesktop
kubectl create -f http://abcdesktopio.github.io/setup/abcdesktop.yaml

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] 
then
        echo "'kubectl create -f http://abcdesktopio.github.io/setup/abcdesktop.yaml' command was successful"
else
        echo "'kubectl create -f http://abcdesktopio.github.io/setup/abcdesktop.yaml' failed"
        exit $?
fi

# docker pull image core images
REGISTRY_DOCKERHUB="abcdesktopio"
docker pull $REGISTRY_DOCKERHUB:oc.user.18.04
docker pull $REGISTRY_DOCKERHUB:oc.cupsd.18.04
docker pull $REGISTRY_DOCKERHUB:oc.pulseaudio.18.04

# docker pull applications
docker pull $REGISTRY_DOCKERHUB:writer.d 
docker pull $REGISTRY_DOCKERHUB:calc.d 
docker pull $REGISTRY_DOCKERHUB:impress.d 
docker pull $REGISTRY_DOCKERHUB:firefox-esr.d 
docker pull $REGISTRY_DOCKERHUB:gnome-terminal.d
docker pull $REGISTRY_DOCKERHUB:gimp.d

kubectl get pods --namespace=abcdesktop

echo "Setup done"
echo "Open your navigator to http://[your-ip-hostname]:30443/"

