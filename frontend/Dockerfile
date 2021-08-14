FROM node:latest as builder
LABEL org.opencontainers.image.source=https://github.com/hsheth2/ppa-stats

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . ./
RUN yarn build

FROM nginx
COPY --from=builder /app/dist /usr/share/nginx/html
