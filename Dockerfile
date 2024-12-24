# Use the official .NET SDK image
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build-env

# Set the working directory inside the container
WORKDIR /app

# Copy the .csproj file and restore dependencies
COPY src/ProjectName/*.csproj ./
RUN dotnet restore

# Copy the entire project
COPY . ./

# Build the project
RUN dotnet publish -c Release -o out

# Set the entry point for the container
ENTRYPOINT ["dotnet", "out/ProjectName.dll"]
