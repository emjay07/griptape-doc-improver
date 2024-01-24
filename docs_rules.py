from dotenv import load_dotenv

from griptape.loaders import WebLoader
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import TaskMemoryClient, FileManager

# Load your environment
load_dotenv() 

# load in the documentation page you want to improve
# TODO: Make this parameter
docs_pages = WebLoader().load(
    "https://docs.griptape.ai/latest/griptape-framework"
)

# original ruleset for writing guidance
doc_improver_ruleset = Ruleset(
    name="doc_improver",
    rules=[
        Rule("You are helping improve technical documentation for an open source code library written in python."),
        Rule("The target audience for the coding library are beginner python developers."),
        Rule("You should suggest spelling and grammar updates."),
        Rule("You should always suggest specific examples on how to improve the documentation"),
    ]
)

# new ruleset to rewrite
doc_rewriter_ruleset = Ruleset(
    name="doc_improver",
    rules=[
        Rule("You are helping improve technical documentation for an open source code library written in python."),
        Rule("The target audience for the coding library are beginner python developers."),
        Rule("Only answer in markdown format."),
    ]
)

# agent to run the rules
# TODO: make the file name a parameter
agent = Agent(
    input_template="Rewrite the following documentation page {{ args[0] }} to follow documentation best practices and save in doc_rewrite_rules.md",
    rulesets = [
        doc_rewriter_ruleset
    ],
    tools = [TaskMemoryClient(off_prompt=False), FileManager()]
)

agent.run(docs_pages)
