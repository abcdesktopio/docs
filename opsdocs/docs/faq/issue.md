---
title: Known Issues & Troubleshooting | abcdesktop.io
description: Known issues, workarounds, and troubleshooting tips for common abcdesktop.io deployment and runtime problems.
keywords: issues, troubleshooting, known issues, workarounds, abcdesktop, Kubernetes, debugging
tags:
  - FAQ
  - troubleshooting
  - issues
---

# GitHub Issues

## How to Request a New Feature

Submit a feature request in the `conf` GitHub repository: [Ask a Feature](https://github.com/abcdesktopio/conf/issues)

When creating the issue:
- Clearly describe the desired behavior or capability.
- Tag the issue as **feature** using the **type** field on the right.

## How to Report an Issue

Submit a bug report in the `conf` GitHub repository: [Create an Issue](https://github.com/abcdesktopio/conf/issues)

**Required information:**

1. **`od.config` file** — Extract the current configuration:

   ```bash
   NAMESPACE=abcdesktop
   kubectl -n $NAMESPACE get configmap abcdesktop-config -o jsonpath='{.data.od\.config}' > od.config
   ```

2. **`abcdesktop.yaml` file** — Include the Kubernetes manifest used for your deployment.

3. **Expected behavior** — Describe what you expected to happen.

4. **Actual behavior** — Describe what actually happened, including any error messages, log output, or screenshots.
