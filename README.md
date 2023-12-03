# whatsapp_clone_api
A clone for whatsapp to chat and create rooms to chat in
available endpoints nclude : 
**Auth**
POST
Registraton

*typically looks like*
json
{
    "username": "name",
    "password1": "pass",
    "password2": "pass",
    "email": "test@test.com"
}
Login
*typically looks like*
json
{
    "username":"name",
    "password":"pass"
    }

**Chat**
POST
Start Conversation
*requires auth*
GET
Get Conversation
GET
Conversations
GET
New Request
