# Dockerfile - Selenium 

#FROM selenium/standalone-chrome:latest
FROM selenium/standalone-chrome:latest

# Defina o diretório de trabalho
WORKDIR /home/seluser/etl_ca

# Copia script.py para diretório
COPY script_etl.py /home/seluser/etl_ca
COPY transform_loading_process.py /home/seluser/etl_ca
COPY requirements.txt /home/seluser/etl_ca

# Diretório para download
RUN sudo mkdir /downloads

# Instale o Python e as bibliotecas Selenium e Requests
RUN sudo apt-get update && sudo apt-get install -y python3 python3-pip  
RUN pip install -r requirements.txt

# Instala Locale 
RUN sudo apt-get install -y locales && sudo rm -r /var/lib/apt/lists/*

# configura Locale
RUN sudo sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    sudo dpkg-reconfigure --frontend=noninteractive locales

# Define o fuso horário como America/Sao_Paulo
ENV TZ=America/Sao_Paulo
USER root
RUN apt-get install -y tzdata
RUN cp /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

# Retorna para o usuário padrão do container
USER seluser
RUN echo "export TZ=${TZ}" >> ~/.bashrc 

# Execute o script quando o contêiner for iniciado
CMD ["python3", "script_etl.py"]










