FROM golang:1.14-alpine as build

COPY . /go/src/gitlab.com/isard-vdi/isard/websockify
WORKDIR /go/src/gitlab.com/isard-vdi/isard/websockify

RUN go env -w GOPROXY=https://goproxy.cn,direct
RUN go build -o websockify main.go


FROM alpine:3.11.3


COPY --from=build /go/src/gitlab.com/isard-vdi/isard/websockify/websockify /

CMD [ "/websockify" ]
