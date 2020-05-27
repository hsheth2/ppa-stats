FROM node

WORKDIR /app/backend

COPY package.json yarn.lock ./
RUN yarn

COPY . ./

EXPOSE 8000
CMD [ "node", "app.js" ]
