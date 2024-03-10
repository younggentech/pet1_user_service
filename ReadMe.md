# User microservice
This repository is a part of the system to help students easily form groups for assignments.
The microservice will handle registration and all processes connected to user profiles.
## API Structure:
1. User API. <br>
**Scope:** Create, Verify, Delete, Update a user profile. Get a JWT for a user.<br>
**Workflow:** Create -> Verify -> Modify -> Delete. Before, the user is verified, they can't get a token.


