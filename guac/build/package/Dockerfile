#
# Build phase
#
FROM golang:1.16-alpine as build

RUN apk add --no-cache \
    git

COPY . /build
WORKDIR /build

RUN go env -w GOPROXY=https://goproxy.cn,direct
RUN go build -o guac cmd/guac/guac.go

#
# Guac
#
FROM alpine:3.13

COPY --from=build /build/guac /guac

EXPOSE 4567

CMD [ "/guac" ]
