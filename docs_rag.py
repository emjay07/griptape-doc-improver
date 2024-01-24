from dotenv import load_dotenv

from griptape.loaders import WebLoader
from griptape.structures import Agent
from griptape.tools import WebScraper, TaskMemoryClient, VectorStoreClient, FileManager
from griptape.tasks import PromptTask, ToolkitTask
from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver
from griptape.engines import VectorQueryEngine

# Load your environment
load_dotenv()  

# constants
MAX_TOKENS = 1000
NAMESPACE1 = "django"

def insert_page(engine, url, namespace):
    engine.upsert_text_artifacts(
        WebLoader(max_tokens=MAX_TOKENS).load(url), namespace=namespace
    )

engine = VectorQueryEngine(
    vector_store_driver=LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver())
)

# could expand this to load more pages
insert_page(engine, "https://docs.djangoproject.com/en/5.0/", NAMESPACE1)
insert_page(engine, "https://docs.djangoproject.com/en/5.0/intro/overview/", NAMESPACE1)

vector_db = VectorStoreClient(
    description="This store has django's documentation",
    query_engine=engine,
    namespace=NAMESPACE1,
)

# agent to read django's documentation and create rules
loader_agent = Agent(
    input_template="Based on django's documentation, create a set of rules that all documentation should follow.",
    tools=[vector_db, TaskMemoryClient(off_prompt=False)]
)

loader_response = loader_agent.run()

# agent to rewrite input based on the rules from the loader agent
rewrite_agent = Agent(
    tasks=[
        PromptTask(
            "Rewrite the following documentation: {{ args[0] }}, using the documentation guidelines: {{ doc_guidelines }}",
            context={
                "doc_guidelines": loader_response.output_task.output.value,
            },
        )
    ],
    task_memory=loader_response.task_memory,
    tools=[TaskMemoryClient(off_prompt=False), WebScraper()]
)

rewrite_response = rewrite_agent.run("https://docs.griptape.ai/latest/griptape-framework")

# agent to write to a file
output_agent = Agent(
    tasks=[
        ToolkitTask(
            "Write \"{{ output }}\" to a file called {{ args[0] }}",
            context={
                "output": rewrite_response.output_task.output.value,
            },
            tools=[FileManager()]
        )
    ]
)

output_agent.run("docs_rewrite_rag_agents.md")