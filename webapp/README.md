# Vue webapp for displaying sensor data

This webapp can stream live data, fetch historical data, initiate CSV file downloads for historical data fetched from the backend service and display information about the sensors connected to the machine running the backend service.

User settings such as the host and port of the backend service are stored on the user's machine and by that are persistent over multiple sessions.

<br>

# Installation

The necessary dependencies will be installed by the following command

```
npm install
```

<br>

# Configuration

By providing a `.env` or `.env.local` file in the root directory environment variables can be provided.

The following are available:

VUE_APP_DEFAULT_SERVER_HOST: (optional) the default host address that should be used to connect to the backend service when the user has not manually entered a host yet

VUE_APP_DEFAULT_SERVER_PORT: (optional) the default port on the host that should be used to connect to the backend service when the user has not manually entered a port yet

<br>

# Running

## Development mode

with hot reloading when code is changed

```
npm run serve
```

<br>

## Production mode

Compile code and assets into the dist directory:


```
npm run build
```

<br>

Run the compiled code:

```
npm run serve:dist
```

<br>

## Alternative to webapp: building as electron desktop app

By using electron and electron-builder via vue-cli-plugin-electron-builder this webapp can be bundled into an executable as a standalone desktop application.

Run `npm run electron:serve` for development mode.

Run `npm run electron:build -- -mwl` to build executable packages for Mac, Window and Linux. More information on parameters at: [electron.build/multi-platform-build](https://www.electron.build/multi-platform-build)