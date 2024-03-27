import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

class Query(graphene.ObjectType):
    # Define a Field 'hello' in our Schema with a single Argument 'name'
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    # Resolver method takes GraphQL context (root/self/parent, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    # Type hints: For instance methods, omit type for "self"
    # JS/Prisma equivalent: (obj/parent, args, context, info)
    async def resolve_hello(self, info, name):
        # We can make asynchronous network calls here
        return f"Hello {name}"


schema = graphene.Schema(query=Query)

app = FastAPI()
app.add_route("/", GraphQLApp(schema=schema))