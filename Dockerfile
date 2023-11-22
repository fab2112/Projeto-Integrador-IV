# Dockerfile - Dashboard 

# Pull imagem base
FROM python:3.11-slim

# Garante que a saída do Python seja imediatamente escrita no stdout/stderr e não armazenada em buffer:
ENV PYTHONUNBUFFERED=1

# Cria diretório de trabalho (container python)
RUN mkdir -p /home/dashboard

# Define o diretório de trabalho
WORKDIR /home/dashboard

# Crie um usuário não-root (dashuser) e grupo (dashuser)
RUN groupadd -r dashuser && useradd --no-log-init -r -g dashuser dashuser

# Altere a propriedade do diretório do aplicativo para o novo usuário
RUN chown -R dashuser:dashuser /home/dashboard

# Adiciona o diretório de instalação do gunicorn ao $PATH
ENV PATH="/home/dashboard/venv/bin:${PATH}"

# Copia tudo para diretório projeto (container python)
COPY /assets/*.* /home/dashboard/assets/
COPY /components/*.* /home/dashboard/components/
COPY /utils/*.* /home/dashboard/utils/
COPY /layout/*.* /home/dashboard/layout/
COPY app.py /home/dashboard
COPY requirements.txt /home/dashboard
COPY settings.py /home/dashboard

# Adiciona pacote de sistema ausente
RUN apt-get update && \
    apt-get install -y libgssapi-krb5-2 && \
    rm -r /var/lib/apt/lists/*

# Instala Locale 
RUN apt-get update && apt-get install -y \
    locales && rm -r /var/lib/apt/lists/*
# configura Locale
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

# Define o fuso horário como America/Sao_Paulo
ENV TZ=America/Sao_Paulo
RUN apt-get install -y tzdata
RUN cp /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

# Crie um ambiente virtual, ative-o como o usuário appuser e instala as dependências
RUN su dashuser -c "python3 -m venv venv"
RUN su dashuser -c ". venv/bin/activate && pip install --upgrade pip && pip install wheel && pip install -r requirements.txt"

USER dashuser

# Run in background docker run --name dashboard -d -p 8050:8050  dashboard:latest
CMD ["gunicorn", "-b", "0.0.0.0:8085", "--workers", "4", "--threads", "20", "app:server"]