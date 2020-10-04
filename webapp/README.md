# Vue webapp for displaying sensor data

This webapp can stream live data, fetch historical data, initiate CSV file downloads for historical data fetched from the backend service and display information about the sensors connected to the machine running the backend service.

The graphs are SVGs generated with the help of Vue's reactivity system and the data is transferred via websockets.

User settings such as the host and port of the backend service are stored on the user's machine and by that are persistent over multiple sessions.

<br>

### Project setup
```
npm install
```

<br>

### Compiles and hot-reloads for development
```
npm run serve
```

<br>

### Compiles and minifies for production
```
npm run build
```

<br>

### Lints and fixes files
```
npm run lint
```

<br>

### Configuration

By providing a `.env` or `.env.local` file in the root directory environment variables can be provided.

The following are available:

VUE_APP_DEFAULT_SERVER_HOST: (optional) the default host address that should be used to connect to the backend service when the user has not manually entered a host yet

VUE_APP_DEFAULT_SERVER_PORT: (optional) the default port on the host that should be used to connect to the backend service when the user has not manually entered a port yet

<br>

### Build as electron desktop app

By using electron and electron-builder via vue-cli-plugin-electron-builder this webapp can be bundled into an executable as a standalone desktop application.

Run `npm run electron:serve` for development mode.

Run `npm run electron:build -- -mwl` to build executable packages for Mac, Window and Linux. More information on parameters at: [electron.build/multi-platform-build](https://www.electron.build/multi-platform-build)