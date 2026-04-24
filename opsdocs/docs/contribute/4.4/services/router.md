# Route - OpenResty HTTP Router

## Project Specification

### Purpose

`route` is an OpenResty-based HTTP reverse proxy designed for the abcdesktop platform. It provides secure, JWT-authenticated routing to user desktop containers running in Kubernetes.

---

## Architecture Overview

```
┌─────────────────┐
│   Client        │
│   (Browser)     │
└────────┬────────┘
         │ HTTP Request + JWT
         ▼
┌─────────────────────────────────────────────────────────┐
│                    route (OpenResty)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  get.targetmap.lua                                │  │
│  │  - Extract JWT from request                       │  │
│  │  - Verify JWT signature                           │  │
│  │  - RSA Decrypt payload to get target hostname     │  │
│  │  - Cache result in shared dict (10 min)           │  │
│  └───────────────────────────────────────────────────┘  │
└────────┬────────────────────────────────────────────────┘
         │ $target variable resolved
         ▼
┌─────────────────────────────────────────────────────────┐
│     Pods (Kubernetes)                                   │
│     ┌──────────────────────┐                            │
│     │      Desktop Pod     │                            │
│     │  service TCP port    │                            │
│     └──────────────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

---

## Detailed Analysis: `get.targetmap.lua`

### Role

This Lua script is the core authentication and routing engine. It executes during the `rewrite` phase for protected endpoints and resolves the `$target` nginx variable used in `proxy_pass` directives.

### Execution Flow

```
1. Extract JWT token from request
         │
         ▼
2. Check targetmap cache
   ┌──────────────┐
   │ Cache Hit?   │──Yes──→ Set $target → Continue request
   └──────────────┘
         │ No
         ▼
3. Read public key from env or cache
         │
         ▼
4. Verify JWT signature
         │
         ▼
5. Decrypt payload.hash using dedicated RSA private key
         │
         ▼
6. Cache result in targetmap (TTL: min(exp-now, 600s))
         │
         ▼
7. Set $target = decrypted hostname
```

### Code Walkthrough

#### 1. Token Extraction

```lua
local jwt_token = ngx.var.jwt_token
```

The token is sourced from:
- Query parameter: `?jwt_token=xxx`
- Header: `Authorization: Bearer <token>`
- Header: `AbcAuthorization: <token>`

The `no_bearer()` function strips the "Bearer " prefix if present.

#### 2. Response Helper

```lua
function ngxexitresponse(status, msg)
    ngx.status = status
    ngx.log(ngx.ERR, msg)
    ngx.say(msg)
    ngx.exit(ngx.HTTP_OK)
end
```

Returns HTTP error responses with logging. Uses `ngx.exit(ngx.HTTP_OK)` after setting `ngx.status` to properly interrupt execution.

#### 3. RSA Decryption

```lua
local function decrypt(msg, private_key)
    local rsa = require "resty.rsa"
    local priv, err = rsa:new({ private_key = private_key })
    local crypto = ngx.decode_base64(msg)
    local decrypted, err = priv:decrypt(crypto)
    return decrypted
end
```

The JWT payload contains a `hash` field that is:
1. Base64-encoded
2. RSA-encrypted with the server's public key
3. Contains the target pod hostname

#### 4. Cache Lookup

```lua
local target = ngx.shared.targetmap:get(jwt_token)
```

The `targetmap` shared dictionary (8MB) caches resolved targets to avoid repeated JWT processing.

#### 5. JWT Verification

```lua
local jwt = require "resty.jwt"
local jwt_secret = ngx.shared.rsakeymap:get('jwt_desktop_signing_public_key')
  or readfile(os.getenv("JWT_DESKTOP_SIGNING_PUBLIC_KEY"))

local jwt_obj = jwt:verify(jwt_secret, jwt_token)
```

Verifies the JWT signature using the configured RSA public key.

#### 6. Payload Decryption & Caching

```lua
local private_key = ngx.shared.rsakeymap:get('jwt_desktop_payload_private_key')
  or readfile(os.getenv("JWT_DESKTOP_PAYLOAD_PRIVATE_KEY"))

target = decrypt(payload.hash, private_key)

-- Cache with TTL
local expire_value = payload.exp - ngx.time()
if expire_value > 600 then expire_value = 600 end
if expire_value > 1 then
    ngx.shared.targetmap:set(jwt_token, target, expire_value)
end
```

**Cache TTL Logic:**

- Uses JWT `exp` claim for expiration
- Capped at 600 seconds (10 minutes) maximum
- Minimum 1 second required to cache
- Prevents caching of expired/invalid tokens

#### 7. Target Assignment

```lua
ngx.var.target = target
```

Sets the nginx variable used by `proxy_pass http://$target:$port/`

---

## Endpoint Routing Table


### Service Endpoints

| Endpoint | Service Variable | Default Port | Protocol |
|----------|-----------------|--------------|----------|
| `/spawner` | `$spawner_service_tcp_port` | 29786 | HTTP |
| `/terminals` | `$xterm_tcp_port` | 29781 | WebSocket |
| `/terminals/{id}/size` | `$xterm_tcp_port` | 29781 | HTTP |
| `/filer` | `$file_service_tcp_port` | 29783 | HTTP (8GB max) |
| `/printerfiler` | `$printerfile_service_tcp_port` | 29782 | HTTP |
| `/websockify` | `$ws_tcp_bridge_tcp_port` | 6081 | WebSocket |
| `/signalling` | `$signalling_service_tcp_port` | 29787 | WebSocket |
| `/broadcast` | `$broadcast_tcp_port` | 29784 | WebSocket |
| `/sound` | `$sound_service_tcp_port` | 29788 | WebSocket |
| `/microphone` | `$microphone_service_tcp_port` | 29789 | WebSocket |
| `/gamepad` | `$gamepad_service_tcp_port` | 29790 | WebSocket |
| `/snapshot` | `$snapshot_service_tcp_port` | 29785 | HTTP |
| `/console` | `console` upstream | - | HTTP |

### pyos Endpoints

Pattern proxy_pass backend: `http://$pyos_fqdn:$pyos_service_port`:

- `/API/manager/image` with client_max_body_size 16m;
- `/API/composer/launchdesktop` with proxy_read_timeout 600s;
- `/API` 

### Utility Endpoints

| Endpoint | Description |
|----------|-------------|
| `/healthz` | Health check, returns "OK" |
| `/node` | Returns `NODE_NAME` environment variable |
| `/.well-known/*` | Let's Encrypt ACME challenges |
| `/speedtest` | Raw data throughput testing (no gzip) |
| `/` | Default website content |

---

## Configuration Files

### `nginx.conf` - Main Configuration

**Key directives:**

- `worker_processes auto` - Scales to available CPUs
- `daemon off` - Required for container foreground execution
- `env` directives - Exposes environment variables to nginx

- **Lua shared dictionaries:**
  - `rsakeymap` (1MB) - RSA key content cache
  - `rsafilenamekeymap` (1MB) - Key filename mappings
  - `targetmap` (8MB) - JWT → target resolution cache

**Security settings:**

- `server_tokens off` - Hides nginx version
- `more_clear_headers Server` - Removes Server header
- `TLS 1.2+` with strong cipher suite

### `sites-enabled/routehttp.conf` - Server Block

**Initialization:**

```lua
init_by_lua_block {
  pyos_fqdn = os.getenv("PYOS_FQDN") or "pyos"
  pyos_service_port = os.getenv("PYOS_SERVICE_PORT") or "8000"
}
```

**Service port variables:**

```nginx
set $ws_tcp_bridge_tcp_port             6081;
set $xterm_tcp_port                     29781;
set $file_service_tcp_port              29783;
# ... etc
```

**Listening:**

- Port 80 (HTTP)
- Port 443 (HTTPS, commented out by default)

### `proxy.conf` - Standard Proxy Headers

```nginx
proxy_set_header User-Agent            $http_user_agent;
proxy_set_header Origin                $http_origin;
proxy_set_header X-Real-IP             $remote_addr;
proxy_set_header X-Forwarded-For       $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Host      $server_name;
proxy_set_header Accept-Language       $http_accept_language;
proxy_set_header Host                  $host;
```

### `ws.conf` - WebSocket Configuration

```nginx
sendfile off;
tcp_nopush off;
proxy_buffering off;
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

---

## Docker Images

### Default Image (Ubuntu Jammy)

```dockerfile
FROM openresty/openresty:jammy
```

**Packages installed:**

- lua-resty-jwt
- lua-resty-string
- lua-cjson
- lua-resty-rsa
- lua-resty-dns

### Alpine Image

```dockerfile
FROM openresty/openresty:alpine
```

**Additional tools:**

- certbot (Let's Encrypt)

**Build approach:**

- Installs build dependencies, compiles LuaRocks packages, removes build tools

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NODE_NAME` | No | - | Node identifier for `/node` endpoint |
| `JWT_DESKTOP_PAYLOAD_PRIVATE_KEY` | Yes | - | Path to RSA private key for payload decryption |
| `JWT_DESKTOP_SIGNING_PUBLIC_KEY` | Yes | - | Path to RSA public key for signature verification |
| `PYOS_SERVICE_PORT` | No | 8000 | PyOS backend port |
| `PYOS_FQDN` | No | `pyos` | PyOS backend hostname |
| `NAMESERVER_RESOLVER` | No | From `/etc/resolv.conf` | DNS resolver for nginx |

---

## Security Considerations

1. **JWT Validation Chain**
   - Signature verification with RSA public key
   - Payload decryption with RSA private key
   - Expiration validation via cache TTL

2. **Information Disclosure Prevention**
   - Server version hidden
   - Error messages logged but minimal in response

3. **Resource Limits**
   - Upload limits: 8MB (spawner), 8GB (filer)
   - Cache TTL capped at 10 minutes
   - Shared dictionary sizes bounded

4. **WebSocket Security**
   - Proper Upgrade/Connection headers
   - Buffering disabled for real-time communication

---

## Logging

- **Access log:** `/var/log/nginx/access.log`
- **Error log:** `/var/log/nginx/error.log`
- **JWT errors:** Logged at `ngx.ERR` level
- **Cache hits:** Logged at `ngx.NOTICE` level with TTL and target

## Rebuild the container images

- from `openresty/openresty` alpine
  
```
git clone -b https://github.com/abcdesktopio/route.git route
cd route
REPO=abcdesdesktop
docker build -t $REPO/route:4.4 -f Dockerfile.alpine --build-arg BASE_IMAGE_RELEASE=alpine --build-arg BASE_IMAGE=openresty/openresty .
```
