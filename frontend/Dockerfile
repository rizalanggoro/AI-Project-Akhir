FROM node:24.3-alpine3.22 AS builder

WORKDIR /app

# copy package*.json untuk menginstall dependencies
COPY package*.json .

# install dependencies
RUN npm install

# copy semua file dari direktori lokal ke dalam image
COPY . .

# set environment variable untuk VITE_API_URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# build aplikasi
RUN npm run build

# menggunakan nginx sebagai web server
FROM nginx:1.29-alpine3.22

# copy hasil build dari builder stage ke nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# run frontend
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
