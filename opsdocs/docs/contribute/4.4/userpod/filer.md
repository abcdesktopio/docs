---
title: Filer Container — File Transfer Service | abcdesktop.io
description: Developer reference for the abcdesktop.io filer container: file upload, download, ZIP archive, and directory listing over HTTP within the user pod.
keywords: filer, file transfer, upload, download, ZIP, abcdesktop, contribute, user pod
tags:
  - contribute
  - filer
  - file transfer
  - user pod
---

# File Service Implementation Specification

## 1. Scope

This document specifies the runtime behavior of the file service implemented in `file-service.js`. It is an implementation-driven specification.

Primary capabilities:

- Upload a file to a path under the user home directory.
- Download a file.
- Download a directory as a generated zip stream.
- List files in a directory.
- Delete a file.

## 2. Runtime Architecture

### 2.1 Process model

- The service runs as a single Node.js process; the Express application and router are initialized in `file-service.js`.
- TCP socket binding is delegated to the external helper function `listenDaemonOnContainerIpAddr`.
- All uncaught exceptions are logged but do not trigger an explicit shutdown sequence.

### 2.2 Router mounting

- Router is mounted under a regex prefix in `file-service.js`:
  - /filer
  - /printerfiler
- Therefore, route path `/` in router effectively maps to `/filer` and `/printerfiler` at runtime.

### 2.3 Middleware chain

Global middleware in order:

1. `helmet()` security headers.
2. `express.json()` body parser.
3. Request logger.

Route-specific validation middleware comes from `middlewares.js`:

- Query validator for `file`.
- Body validator for `file`.
- Query validator for `directory`.
- Multipart uploaded file structural validator.

Error handling:

- Per-route async exceptions are wrapped by `express-async-handler`.
- Global error handler returns 500 with fixed payload in `file-service.js`

## 3. Configuration Specification

### 3.1 Environment variables

- Root directory: `HOME` read.
- Listen port: `FILE_SERVICE_TCP_PORT` fallback 29783.
- Feature toggles:
  - `SENDFILE`
  - `ACCEPTFILE`
  - `ACCEPTLISTFILE`
  - `ACCEPTDELETEFILE`

### 3.2 Toggle interpretation

`is_allow_var` maps values as follows:

- **Deny** when the value (case-insensitive) is one of: `0`, `false`, `disable`, `disabled`.
- **Allow** otherwise, including when the variable is undefined.

Default behavior: all features are enabled unless explicitly disabled via environment variable.

## 4. Security and Path Confinement Model

### 4.1 Intended boundary

All filesystem operations are intended to stay under `HOME` using:

- `checkSafePath`
- `normalize_tildpath`

### 4.2 Path normalization rules

`normalize_tildpath` behavior:

- Expands a leading `~` to the value of `HOME`.
- Applies `path.normalize`.
- If the resolved directory falls outside `HOME`, it prepends `HOME` and normalizes the result again.

### 4.3 Path safety predicate

`checkSafePath` behavior:

- Expands a leading `~` to the value of `HOME`.
- Normalizes the path.
- Returns `true` when either the resolved directory starts with `HOME`, or the original `currentPath` exactly equals `HOME`.

## 5. Data and I/O Behavior

### 5.1 Upload buffering

- Multer is configured with in-memory storage.
- Uploaded file content is fully buffered in RAM before being written to disk.

### 5.2 File streaming

- File download uses stream pipeline.
- Zip download uses JSZip node stream.

### 5.3 Zip generation

- Recursive directory traversal is implemented by `generateZipTree`.
- Folder names are split on `/` (non-portable if run outside POSIX path semantics).
- Read errors are logged and swallowed inside the recursion; the operation continues on remaining entries.

### 5.4 Directory listing sort

- The directory listing is sorted in ascending order by file modification time.
- If a file's `stat` call fails, the file receives a synthetic modification time of `0` and will likely appear first in the sorted result.

## 6. API Contract (Implementation Accurate)

Base route prefix: /filer and /printerfiler.

### 6.1 GET /

Resolved endpoints:

- GET /filer
- GET /printerfiler

Purpose:

- Download a file, or if path is a directory, download a generated zip.

Input:

- Query parameter `file` required, non-empty string validated by middleware.

Flow:

1. Check `SENDFILE` toggle.
2. Validate path via `checkSafePath`.
3. Normalize path.
4. Check existence.
5. If file: stream bytes.
6. If directory: generate zip recursively and stream zip.

Responses:

- 200: binary stream (file bytes or zip bytes).
- 400: feature disabled or unsafe path.
- 404: path not found.
- 422: validator errors when query is missing/invalid.
- 500: unhandled runtime exception.

Headers on directory download:

- Content-Disposition: attachment; filename="<normalized-path>.zip"
- Content-Type: application/zip


### 6.2 GET /directory/list

Resolved endpoints:

- GET /filer/directory/list
- GET /printerfiler/directory/list

Purpose:

- Return sorted file names of a directory.

Input:

- Query parameter `directory` required, non-empty string.

Flow:

1. Check `ACCEPTLISTFILE` toggle.
2. Validate safe path.
3. Normalize path.
4. Check existence and directory type.
5. Return sorted names.

Responses:

- 200: JSON array of filenames.
- 400: feature disabled or unsafe path.
- 404: path not found or path not a directory.
- 422: validator errors when query is missing/invalid.
- 500: unhandled runtime exception.


### 6.3 POST /

Resolved endpoints:

- POST /filer
- POST /printerfiler

Purpose:

- Upload multipart file field named `file` and save under HOME boundary.

Input:

- Multipart field `file` required.
- Optional body field `fullPath`:
  - If absent/empty, destination path is original uploaded filename.
  - If provided, destination is that value.

Flow:

1. Parse multipart to memory.
2. Validate uploaded file object shape.
3. Check `ACCEPTFILE` toggle.
4. Normalize destination path.
5. Validate safe path.
6. Ensure destination directory exists (create recursively).
7. Write file bytes.

Responses:

- 200: `{ "code": 200, "data": "ok" }`
- 400: feature disabled (note payload still says code 403).
- 403: unsafe path in default ret object.
- 422: missing/invalid multipart `file` field.
- 500: unhandled runtime exception.


### 6.4 DELETE /

Resolved endpoints:

- DELETE /filer
- DELETE /printerfiler

Purpose:

- Delete a file path under HOME.

Input:

- JSON body field `file` required, non-empty string.

Flow:

1. Validate body.
2. Check `ACCEPTDELETEFILE` toggle.
3. Validate safe path.
4. Normalize path.
5. If exists, unlink.

Responses:

- 200: `{ "code": 200, "data": "ok" }`
- 400: feature disabled or unsafe path.
- 404: file not found.
- 422: missing/invalid body.
- 500: unhandled runtime exception.

### 6.5 Fallback route

- Any unmatched route under mounted prefixes returns:
  - `{ "code": 404, "data": "Can not <METHOD> <PATH>" }`


## 7. Validation Specification


Rules:

- Query `file`: required, string, not empty.
- Body `file`: required, string, not empty.
- Query `directory`: required, string, not empty.
- Multipart upload: `req.file` must exist and include `originalname` string and `buffer` Buffer.

Error format examples:

- Express-validator based 422 shape with `errors` array.
- Upload structural validation also returns 422 with `errors` array.

## 8. Error Contract Matrix

Matrix:

- Validation failure: 422
- Unsafe path: 400 + Path Server Error
- Feature disabled: 400 + Forbidden payload code 403
- Missing resource: 404
- Unmatched path: 404
- Unhandled error: 500

## 9. Operational Characteristics

### 9.1 Logging

- Logs include method/path, paths, and internal errors.
- Sensitive absolute paths may appear in logs.


## 10. Test-Derived Behavioral Expectations

- Upload requires multipart `file` and supports `fullPath` with `~` expansion.
- Download rejects paths outside HOME.
- List endpoint returns 400 for unsafe traversal attempts.
- Delete returns 200 on first success and 404 on second attempt.
