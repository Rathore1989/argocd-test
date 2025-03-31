# Use official PostgreSQL image
FROM postgres:13-alpine

# Environment variables for initialization
ENV POSTGRES_DB=mydb
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password

# Expose the PostgreSQL port
EXPOSE 5432

# Add initialization scripts if needed
COPY init.sql /docker-entrypoint-initdb.d/
