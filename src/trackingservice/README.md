# TrackingService

The Tracking service processes personal information which is then used to calculate the shortest car route from source to destination.

## Local

Run the following command to restore dependencies to `vendor/` directory:

    dep ensure --vendor-only

## Build

From `src/trackingservice`, run:

```
docker build ./
```

## Test

```
go test .
```
