FROM python:slim
RUN apt-get update && apt install curl apt-transport-https gnupg wget lsb-release -y
#RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key |  apt-key add -
RUN curl -sSfL https://aquasecurity.github.io/trivy-repo/deb/public.key |  apt-key add -
RUN echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main |  tee -a /etc/apt/sources.list.d/trivy.list
RUN apt-get update && apt-get install unzip trivy default-jre python3-bandit git -y
#git
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

RUN wget https://github.com/jeremylong/DependencyCheck/releases/download/v7.1.0/dependency-check-7.1.0-release.zip && unzip dependency-check-7.1.0-release.zip

RUN curl -sfL https://raw.githubusercontent.com/securego/gosec/master/install.sh |  sh -s -- -b /usr/local/bin
RUN wget https://go.dev/dl/go1.18.2.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.18.2.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin

WORKDIR /pipeline
COPY . .
RUN pip install -r requirements
ENTRYPOINT ["bash"]


