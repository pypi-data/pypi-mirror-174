# grpc-helper-api

Shared API files for [GRPC helpers](https://github.com/dynod/grpc-helper)

## Common API

The [common.proto](protos/grpc_helper/api/common.proto) file provides reusable API elements for other services (error codes, return status, etc)

## Server handling API

This API defines a [server handling service](doc/server.md) that can be used to fetch services/components information, and control global server behaviors.

## Config API

This API defines a [config service](doc/config.md) that handles configuration items.

## Logger API

This API defines a [logger service](doc/logger.md) that handles loggers configuration.

## Event API

This API defines an [events service](doc/events.md) that handles a generic event system.
