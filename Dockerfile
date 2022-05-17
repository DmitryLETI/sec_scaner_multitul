FROM python:slim
RUN apt-get update && apt install curl apt-transport-https gnupg lsb-release -y
#RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key |  apt-key add -
RUN curl -sSfL https://aquasecurity.github.io/trivy-repo/deb/public.key |  apt-key add -
RUN echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main |  tee -a /etc/apt/sources.list.d/trivy.list
RUN apt-get update && apt-get install trivy -y
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
WORKDIR /pipeline
COPY . .
#RUN pip install -r requirements.txt
CMD ["app.py"]
ENTRYPOINT ["python"]


#wget 'https://github.com/jeremylong/DependencyCheck/releases/download/v7.1.0/dependency-check-7.1.0-release.zip'
#&& unzip dependency-check-7.1.0-release.zip && ./dependency-check/bin/dependency-check.sh