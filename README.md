# AutoPull
AutoPull utilize the [WebHook API](https://developer.github.com/webhooks/) of GitHib to automatic pull the latest commits from GitHub to your deploy server. It listen on a url. When something happening, GitHub will send a POST request to that url with some payload. It will do some stuff based on those payload.

### Requirements
- requests
- Flask

### Configuration

1. go to https://github.com/{your_github_username}/{repository_name}/settings/hooks/new set Payload URL, Content type, Secret(for security) and the events you interested in(as Push event in this case).
2. configure the config file under the AutoPull directory:
   + url: the notify service provided (I use `ServerChan` in this project. For more detail, check this [documentation](http://sc.ftqq.com/2.version)) 
   + port: set the port AutoPull listen
   + path: this object is a dictionary, and the key is the repository name,the value is the path in your deploy server.
   + secret: the secret token you set in first step

### Practical
I run this monitor program on my deploy server listen to port 6000. I use the subdomain autopull.example.com as the payload url and use the VirtualHost function in Apache redirect the request GitHub sent to AutoPull.

### Update
In some cases, We should pull from a private repository. To authenticate that your have permission to pull from that private repository, We should input our username and password manully. To solve this problem, We can clone and pull repository use `ssh` protocol. The detail tutorial is [here](http://www.keybits.net/2013/10/automatically-use-correct-ssh-key-for-remote-git-repo/). 
