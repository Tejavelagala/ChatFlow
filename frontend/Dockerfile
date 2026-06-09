# Frontend Dockerfile - Vue 3 + Vite (Multi-stage)
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app/frontend

ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_WS_BASE_URL=ws://localhost:8000

ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_WS_BASE_URL=$VITE_WS_BASE_URL

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

# Stage 2: Runtime
FROM node:20-alpine

WORKDIR /app/frontend

RUN npm install -g serve

COPY --from=builder /app/frontend/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
