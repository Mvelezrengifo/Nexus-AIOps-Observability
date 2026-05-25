"""
Apollo Federation configuration for GraphQL.
"""

import strawberry
from typing import List, Optional


@strawberry.federation.type(keys=["id"])
class FederatedEvent:
    """Federated event type for Apollo Federation."""

    id: strawberry.ID

    @classmethod
    def resolve_reference(cls, id: strawberry.ID) -> "FederatedEvent":
        """Resolve federated reference."""
        return cls(id=id)


@strawberry.federation.type(keys=["id"])
class FederatedInsight:
    """Federated insight type for Apollo Federation."""

    id: strawberry.ID

    @classmethod
    def resolve_reference(cls, id: strawberry.ID) -> "FederatedInsight":
        """Resolve federated reference."""
        return cls(id=id)


@strawberry.federation.type(keys=["id"])
class FederatedService:
    """Federated service type for Apollo Federation."""

    id: strawberry.ID
    name: str

    @classmethod
    def resolve_reference(cls, id: strawberry.ID) -> "FederatedService":
        """Resolve federated reference."""
        return cls(id=id, name=f"Service {id}")


def get_federated_schema() -> strawberry.federation.Schema:
    """
    Create federated schema for Apollo Federation.

    This allows the NEXUS GraphQL API to be composed
    with other GraphQL services in a federated architecture.
    """
    from app.api.graphql.schema import Query

    @strawberry.federation.type
    class FederationQuery(Query):
        """Extended query with federation support."""

        @strawberry.field
        def _entities(self, representations: List[dict]) -> List[object]:
            """Resolve federated entities."""
            results = []
            for rep in representations:
                if "id" in rep:
                    results.append(FederatedEvent(id=rep["id"]))
            return results

        @strawberry.field
        def _service(self) -> dict:
            """Return service definition for federation."""
            return {"sdl": "type Query { health: HealthStatus }"}

    return strawberry.federation.Schema(
        query=FederationQuery,
        types=[FederatedEvent, FederatedInsight, FederatedService],
    )