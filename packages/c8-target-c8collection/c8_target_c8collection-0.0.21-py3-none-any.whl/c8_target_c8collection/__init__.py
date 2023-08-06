"""GDN data connector target for C8 collections."""
import pkg_resources
from c8connector import C8Connector, Sample, AttributeType, Schema
from c8connector import ConfigProperty


class C8CollectionTargetConnector(C8Connector):
    """C8CollectionTargetConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "c8collection"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "c8-target-c8collection"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('c8_target_c8collection').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "target"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "GDN data connector target for C8 Collections"

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        pass

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        return []

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        return []

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('region', AttributeType.STRING, True, False,
                           description="Fully qualified region URL.", example="api-sample-ap-west.eng.macrometa.io"),
            ConfigProperty('tenant', AttributeType.STRING, True, False,
                           description="Tenant email address.", example="sample@macrometa.io"),
            ConfigProperty('password', AttributeType.STRING, True, False,
                           description="Tenant password.", example="password"),
            ConfigProperty('fabric', AttributeType.STRING, True, False,
                           description="Fabric name.", example="_system"),
            ConfigProperty('target_collection', AttributeType.STRING, True, True,
                           description="Target collection name", example="SampleCollection")
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return []
