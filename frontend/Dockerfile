FROM node:latest as builder
WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn

COPY . ./
RUN yarn build

FROM nginx
COPY --from=builder /app/dist /usr/share/nginx/html
