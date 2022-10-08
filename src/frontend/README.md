# Build Frontend
docker build -f ./frontend/Dockerfile_FRONTEND --no-cache --progress=plain -t pti_frontend . | more

# Run Frontend
docker run --name pti_frontend -d -p 80:80 pti_frontend