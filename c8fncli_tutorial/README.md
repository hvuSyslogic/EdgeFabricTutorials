C8Fn CLI tutorial
============

C8Fn CLI is a tool to build and deploy serverless-functions to Macrometa Edge Fabric.
The CLI is a convenient way to interact with your functions. You can use it to build or invoke or deploy or remove functions to your server using commandline.

Help for all of the commands supported by the CLI can be found by running:
```bash
$c8fn-cli help or c8fn-cli [command] --help
```
Create a new folder for your work:

```bash
$ mkdir -p ~/hello-pydemo && \
  cd ~/hello-pydemo

```

Now let's scaffold a new Python function using the CLI:
```bash
$c8fn-cli new --lang python hello-pydemo -p macrometa -t testtenant --fabric testdb -g http://fabric.macrometa.io --local false
```

This creates three files for you:

hello-python/handler.py
hello-python/requirements.txt
hello-python.yml

Let's edit the handler.py file:
```python
def handle(req):
    print("Hello! You said: " + req)
```

All your functions should be specified in a YAML file like this - it tells the CLI what to build and deploy onto your OpenFaaS cluster.

Checkout the YAML file hello-python.yml:

```yaml
provider:
  name: c8fn
  gateway: http://fabric.macrometa.io
  tenant: demo
  fabric: testdb
  local: false
functions:
  hello-pydemo:
    lang: python
    handler: ./hello-pydemo
    image: macrometa/hello-pydemo
```
gateway- here we can specify a remote gateway if we need to, what the programming language is and where our handler is located within the filesystem.

functions - this block defines the functions in our stack

lang: python - even though Docker is used behind the scenes to package your function. You don't have to write your own Dockerfile unless you want to.

handler - this is the folder / path to your handler.py file and any other source code you need

image - this is the Docker image name. If you are going to push to the Docker Hub change the prefix from hello-python to include your Docker Hub account - i.e. alexellis/hello-python

tenant - your function is created in this tenant.

fabric - your function is created in this fabric.

local - if false, it specifies that function is deployed in all regions; else only in the region specified in the gateway URL.

###NOTE:
For all commands, you can supply input from the commandline or yaml file or environment variables or default arguments.
You should know the precedence given to the i/p supplied from various sources:
commandline > yaml file > environment variables > default arguments
If you don't supply anything, default arguments are taken.
Environment variables to set for gateway,tenant and fabric are C8Fn_URL, C8_TENANT and C8_FABRIC resp.
Default values for gateway,tenant and fabric are '127.0.0.1:8080', 'guest' and '_system' resp.

So now let's build the function.
```bash
$ c8fn-cli build -f hello-python.yml
```
Output of build function:
```bash
Successfully tagged hello-python:latest
Image: hello-python built.
You'll now see output from the Docker Engine as it builds your function into an image in your local Docker library.
```

Here's how to push the built function to your dockerhub repo:
```bash
c8fn-cli push -f hello-pydemo.yml
```

You have to login to execute the following operations on a function:
1.deploy
2.list
3.invoke
4.remove
Login command is as follows:
```bash
$c8fn-cli login --gateway https://127.0.0.1:8080 --tenant testtenant --fabric testdb --username demouser --password demopassword
```
Here you specify tenant login credentials. Keep in mind all are compulsory parameters.

tenant - tenant where you want to perform aforementioned operations on function.
fabric - fabric where you want to perform aforementioned operations on function.
username - username used to login the tenant
password - password 

Now let's deploy the function:

Example deploy using the parameters in the YAML file:

```bash
$c8fn-cli deploy -f hello-pydemo.yml

```

```bash
$c8fn-cli deploy -f hello-pydemo.yml -t testtenant -g --fabric testdb http://fabric.macrometa.io --local false

```
You can optionally supply commandline tenant, fabric and gateway as well. The commandline options will override the options in the yaml file.
The parameters specified here have mean the same as given in c8fn-cli new command.

Use the list command to check whether function is available:
```bash
$c8fn-cli list -g http://fabric.macrometa.io
```
For this operation , you can specify commandline parameters - tenant, fabric etc.

```bash
$c8fn-cli invoke echo --gateway https://domain:port --tenant testtenant --fabric testdb --content-type application/json --query org=c8fn
```

You can specify content-type or query params or headers (Have a look at the c8fn-cli invoke --help to get a better idea.)


Use the remove command to remove/delete the deployed function:
```bash
$c8fn-cli remove hello-pydemo -g http://fabric.macrometa.io --tenant testtenant --fabric testdb
```

###Templates

Command:
```bash
$c8fn-cli new FUNCTION_NAME --lang python/node/go/ruby/Dockerfile/etc
``` 
In your YAML you can also specify lang: node/python/go/csharp/ruby


