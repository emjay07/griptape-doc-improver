from dotenv import load_dotenv
from rich import print as rprint

from griptape.structures import Workflow
from griptape.tools import WebScraper, TaskMemoryClient, FileManager
from griptape.tasks import PromptTask, ToolkitTask

load_dotenv()

# workflow steps
# 1. Scrape "golden set" docs
# 2. Pull out rules from those docs
# 3. Scrape comparison docs
# 4. Provide feedback on 3 using 2's rules
# new step 4: rewrite docs using the rules from step 2

start_task = PromptTask(
    "I would like specific suggestions on how to improve my documentation based on the style of other documentation I provide you.",
    id="start_analysis",
)

scrape_golden_task = ToolkitTask(
    "Load this documentation page: https://docs.djangoproject.com/en/5.0/intro/overview/", 
    tools=[TaskMemoryClient(off_prompt=False), WebScraper()],
    id="golden_set"
)

build_rules_task = PromptTask(
    "Build a set of documentation guidelines based on the following documentation: {{ parent_outputs }}",
    id="doc_guidelines",
)

scrape_mine_task = ToolkitTask(
    "Load this documentation page and output it verbatim: https://docs.griptape.ai/latest/griptape-framework",
    tools=[TaskMemoryClient(off_prompt=False), WebScraper()],
    id="my_docs",
)

# step to write suggestions
# no longer use this in the final workflow
provide_feedback_task = ToolkitTask(
    "How can I improve the following documentation: {{ parent_outputs['my_docs'] }}, using the documentation guidelines: {{ parent_outputs['doc_guidelines'] }}. Store the suggestions in a file called suggestions.txt.",
    tools=[FileManager(), TaskMemoryClient(off_prompt=False)],
    id="produce_suggestions",
)

# step to rewrite docs
# TODO: make filename an input parameter
rewrite_task = ToolkitTask(
    "Rewrite following documentation: {{ parent_outputs['my_docs'] }}, using the documentation guidelines: {{ parent_outputs['doc_guidelines'] }}. Answer in markdown format and save in a file called docs_rewrite_rag_workflow.md.",
    tools=[FileManager(), TaskMemoryClient(off_prompt=False)],
    id="rewrite",
)

# Workflow creation
workflow = Workflow()
workflow.add_task(start_task)
workflow.add_task(rewrite_task)
workflow.insert_tasks(
    start_task,
    [scrape_golden_task, scrape_mine_task],
    rewrite_task,
    preserve_relationship=True,
)
workflow.insert_tasks(
    scrape_golden_task, [build_rules_task], rewrite_task
)

workflow.run()

# debug
# graph = workflow.to_graph()
# rprint(graph)
