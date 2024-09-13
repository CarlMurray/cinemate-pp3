FROM node:latest
WORKDIR /app
COPY . .
EXPOSE 8000
RUN apt-get update
RUN apt-get install python3
RUN npm i
CMD ["node", "index.js"]