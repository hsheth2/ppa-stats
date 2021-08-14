FROM node
LABEL org.opencontainers.image.source=https://github.com/hsheth2/ppa-stats

WORKDIR /app/backend

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . ./

EXPOSE 8000
CMD [ "node", "app.js" ]
