# eks-iaac
Challenge:
"Using your favourite orchestration tools and platform, provide a working infrastructure-as-code example that provisions a service to execute an implementation of the FizzBuzz coding challenge with documentation on how to use and execute, you may ask one set of clarifying questions if needed.

Solution Description:

I have provisioned AWS EKS cluster and required resources using terraform.
I have developed a python program to implement FizzBuzz challenge, created a Dockerfile to build docker image, generated helm chart to deploy it to the EKS cluster.
Finally I used GitKube to deploy the changes to EKS cluster on every push.
Gitkube is a tool used to deploy applications on a Kubernetes cluster by simply running a git push. I Installed gitkube-cli on my local, gitkube on EKS cluster and configured a remote in my local git repository. Any change pushed to this remote, would automatically gets the latest changes, builds docker image using the dockerfile, pushes the docker image to docker.io and deploys new changes to EKS cluster.


Client side pre-requisites(installation steps):
•	Terraform 
o	brew install terraform
•	Kubectl 
o	brew install kubernetes-cli
•	aws-iam-authenticator (heptio-authenticator)
o	curl -o heptio-authenticator-aws https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/darwin/amd64/heptio-authenticator-aws
o	chmod +x ./heptio-authenticator-aws
o	sudo mv heptio-authenticator-aws /usr/local/bin/
•	git
•	helm (installation steps provided below)
•	gitkube (installation steps provided below)

How to use :
1)	Clone git repository https://github.com/kavithakatepalli/eks-iaac.git 
2)	Provision EKS cluster using the terraform scripts
change to terraform folder and run
a.	Make changes to provider.tf accordingly ((region, optionally profile)
b.	terraform plan
c.	terraform apply
d.	terraform output kubeconfig > ~/.kube/config
e.	terraform output config-map-aws-auth > config-map-aws-auth.yaml
f.	kubectl apply -f config-map-aws-auth.yaml
g.	See nodes coming up using “kubectl get nodes”
3)	Install Helm and Tiller
a.	brew install kubernetes-helm
b.	To create service account and ClusterRoleBinding, run 
i.	kubectl apply -f tiller_rbac.yaml
c.	Secure Tiller installation:     kubectl apply -f ~/environment/rbac.yaml
d.	fizzbuzz folder has the helm chart, go through the values.yml, templates/deployment.yml and service.yml 

4)	gitkube setup
a.	Install gitkube-cli
•	curl https://raw.githubusercontent.com/hasura/gitkube/master/gimme.sh | bash
•	gitkube version # check installation
b.	Install gitkube, select load balancer service type during installation
i.	gitkube install
ii.	kubectl get svc -n kube-system #list the gitkubed service
5)	Generate a Remote spec
Gitkube is configured using the concept of Remotes. A Remote is a Custom Resource in Kubernetes. Each Remote specifies the parameters used to manage the application. Parameters include authentication users for git push access, build definitions, image registry, and runtime arguments.
1)	gitkube remote generate -f myremote.yaml #my inputs are in dark black color
Remote name myremote
Namespacedefault
SSH public key file/Users/kavitha/.ssh/id_rsa.pub
✔ Helm Chart
Manifests/Chart directoryfizzbuzz
✔ Specify a different registry
Docker registry serverhttps://index.docker.io/v1/
Registry URLdocker.io
Usernamekavithakatepalli
Password********
Emailkavitha.thavika@gmail.com
INFO[0029] Created docker-registry secret               
Deployment namefizzbuzz
Container namefizzbuzz
Dockerfile pathDockerfile
Build context path./
✗ Add another container:N
✗ Add another deployment:N
2)	Edit myremote.yml, to add release name for helm chart
helm:
  release: myfizzbuzzrel
3)	Create remote using “gitkube remote create -f myremote.yaml”
4)	Run the last two commands from the output of the above command:
git remote add myremote <remote-url from the output>
         git add *
         git commit -am “deploying to EKS on git push configuration”
         git push myremote master

On push, the Gitkube pipeline kicks in and does a build and deploys application to the cluster.
5)	Access the application
1.	Access the <DNS name of the loadbalancer> in a browser to see the hello page
2.	Access <DNS name of load balancer>/fizzbuzz endpoint to get the fizzbuzz sequence output
3.	Access <DNS name of load balancer>/fizzbuzz?start=<startno>&end=<endno> to print the sequence in range between start and end.



Optionally, we can configure Dashboard and heapster to see what is running in EKS cluster and to get monitoring and performance analysis on the cluster
1)	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
2)	kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/heapster.yaml
3)	kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/influxdb.yaml
4)	kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/rbac/heapster-rbac.yaml
5)	kubectl apply -f eks-admin-service-account.yaml
6)	kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep eks-admin | awk '{print $1}')
7)	kubectl proxy
8)	Access the dashboard http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login 






	






