
![Logo](https://abdelwahab-hamada.github.io/chatta-app/logo192.png)


# chatting app
#### 🔗 [**Chatta fullstack app link**](https://abdelwahab-hamada.github.io/chatta-app/)
## Technologies 
<p align="left"> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a>  <a href="https://graphql.org" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/graphql/graphql-icon.svg" alt="graphql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>   </p>

## API Reference 

- #### **query**
   ###### friends, others:
        -id: ID!
        -username: String!
        -status: String
        -chat: ChatType

 
- #### **mutation**
        -registerMe(username: String!,password: String!)

        -tokenAuth(username: String!,password: String!)

        -joinChat(recipientId: String)

        -sendMessage(recipientId: Stringtext: String)

- #### **subscription**
        -subscribeChat(chatId: String)


## Features

- register
- authintication
- realtime chatting system
- new messages notifications
- user availability status (online,offline)
- messages read recipients system(read,unread,sent,sent-time)

