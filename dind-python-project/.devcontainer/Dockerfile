FROM python:slim

# Ensure all operations are confined to the container
# Removed any unnecessary dependencies to maintain a minimal footprint

# Set locale and timezone
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Set workdir 
WORKDIR /app

# Switch to non-root user for better security
USER $USERNAME

# Add user's bin to PATH
ENV PATH="/home/$USERNAME/.local/bin:${PATH}"