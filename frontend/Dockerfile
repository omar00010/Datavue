FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

# Serve the frontend using a lightweight HTTP server
RUN npm install -g serve
CMD ["serve", "-s", "public"]

EXPOSE 3000