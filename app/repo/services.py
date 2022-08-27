from tracardi.process_engine.action.v1.connectors.trello.credentials import TrelloCredentials
from tracardi.service.plugin.domain.register import FormField, FormGroup, Form, FormComponent, Plugin, Spec, MetaData, \
    Documentation, PortDoc

from app.repo.domain import ServiceConfig, ServiceResource, ServicesRepo, PluginConfig
from app.services import trello


repo = ServicesRepo(
    repo={
        "a307b281-2629-4c12-b6e3-df1ec9bca35a": ServiceConfig(
            name="Trello",
            resource=ServiceResource(
                form=Form(groups=[
                    FormGroup(
                        name="Service connection configuration",
                        description="This service needs to connect to Trello. Please provide API credentials.",
                        fields=[
                            FormField(
                                id="api_key",
                                name="Trello API KEY",
                                description="Please Provide Trello API KEY.",
                                component=FormComponent(type="text",
                                                        props={"label": "API KEY"})
                            ),
                            FormField(
                                id="token",
                                name="Trello TOKEN",
                                description="Please Provide Trello TOKEN.",
                                component=FormComponent(type="text",
                                                        props={"label": "TOKEN"})
                            )
                        ]
                    )]),
                init=TrelloCredentials(
                    api_key="",
                    token=""
                ),
                validator=TrelloCredentials
            ),

            microservice=Plugin(
                start=False,
                spec=Spec(
                    module='tracardi.process_engine.action.v1.microservice.plugin',
                    className='MicroserviceAction',
                    inputs=["payload"],
                    outputs=["response", "error"],
                    version='0.7.2',
                    license="MIT",
                    author="Risto Kowaczewski",
                ),
                metadata=MetaData(
                    name='Trello Microservice',
                    desc='Microservice that runs Trello plugins.',
                    icon='trello',
                    group=["Connectors"],
                    remote=True,
                    documentation=Documentation(
                        inputs={
                            "payload": PortDoc(desc="This port takes payload object.")
                        },
                        outputs={
                            "response": PortDoc(desc="This port returns microservice response."),
                            "error": PortDoc(desc="This port returns microservice error.")
                        }
                    )
                )),
            plugins={
                "a04381af-c008-4328-ab61-0e73825903ce": PluginConfig(
                    name="Add card",
                    validator=trello.add_card.plugin.validate,
                    plugin=trello.add_card.plugin.TrelloCardAdder,
                    registry=trello.add_card.plugin.register()
                )
            }
        )
    })
