# docker-scanner-all_in_one
docker container with some security scaners


Start
_______________________________________________
docker build scanner-tools .
docker run -it scanner-tools
python app.py https://github.com/DmitryPaf/docker-scanner-all_in_one/


Programming language support
_______________________________________________
Go: securego/gosec
Python: PyCQA/bandit
Java: jeremylong/DependencyCheck 
Docker-images: Trivy, Grype
