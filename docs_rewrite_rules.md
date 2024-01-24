# Griptape Framework: A Beginner's Guide                                                                               
                                                                                                                                                    
## Overview                                                                                                            
                                                                                                                    
Welcome to Griptape, a framework designed to help you build AI systems that balance predictability and creativity.     
                                                                                                                    
Griptape provides structure for your AI projects through sequential pipelines, DAG-based workflows, and long-term memory. It also encourages creativity by connecting LLMs (Large Language Models) to external APIs and data stores using tools and short-term memory.                                                                                           
                                                                                                                    
With Griptape, you can easily switch between predictability and creativity based on your project's needs.              
                                                                                                                    
But that's not all! Griptape also helps you manage LLMs effectively by enforcing trust boundaries, schema validation, and tool activity-level permissions. This ensures that your LLMs operate within strict policies while maximizing their reasoning capabilities.                                                                                                
                                                                                                                    
Here are some key principles that guide the design of Griptape:                                                        
                                                                                                                    
- **Modularity and Composability**: All elements of the framework are designed to work independently and can be easily 
combined.                                                                                                              
- **Technology-Agnostic**: Griptape can work with any LLM, data store, or backend through the use of drivers.          
- **Data Security**: Griptape aims to keep data off prompt by default, ensuring secure and low-latency handling of large data.                                                                                                            
- **Minimal Prompt Engineering**: Griptape prefers Python code over natural languages for easier reasoning and debugging.                                                                                                             
                                                                                                                    
## Quick Start                                                                                                         
                                                                                                                    
To get started with Griptape, you'll need to first configure an OpenAI client. This involves [getting an API key](https://platform.openai.com/account/api-keys) and adding it to your environment as `OPENAI_API_KEY`.              
                                                                                                                    
By default, Griptape uses the [OpenAI Completions API](https://platform.openai.com/docs/guides/completion) to execute LLM prompts. However, you can configure other LLMs using [Prompt Drivers](structures/prompt-drivers/).                 
                                                                                                                    
Next, install Griptape using pip or Poetry. If you're using Poetry, create a new project and add Griptape as a dependency.                                                                                                            
                                                                                                                    
## Extras                                                                                                              
                                                                                                                    
Griptape offers a range of functionalities that you can access through the `[all]` [extra](https://peps.python.org/pep-0508/#extras). This is recommended for beginners to get the full Griptape experience.                                                                                                            
                                                                                                                    
If you want to optimize the installation size or only need specific functionalities, you can choose to install only the core dependencies or specific extras. Extras include vendor-specific drivers integrated within the Griptape framework. 
                                                                                                                    
## Building a Simple Agent                                                                                             
                                                                                                                    
With Griptape, you can create structures like [Agents](structures/agents/), [Pipelines](structures/pipelines/), and [Workflows](structures/workflows/) that are composed of different types of tasks. Let's start by building a simple Agent that you can interact with through a chat-based interface.                                                       
                                                                                                                    
Here's a simple example of how to create an Agent and interact with it:                                                
                                                                                                                    
```python                                                                                                              
from griptape.structures import Agent                                                                                  
from griptape.utils import Chat                                                                                        
                                                                                                                    
agent = Agent()                                                                                                        
Chat(agent).start()                                                                                                    
```                                                                                                                    
                                                                                                                    
You can then interact with your model by entering prompts like "Write me a haiku about griptape".                      
                                                                                                                    
## Building a Simple Agent with Tools                                                                                  
                                                                                                                    
You can also add tools to your Agent. Here's an example of an Agent that uses a Calculator tool:                       
                                                                                                                    
```python                                                                                                              
from griptape.structures import Agent                                                                                  
from griptape.tools import Calculator                                                                                  
                                                                                                                    
calculator = Calculator()                                                                                              
agent = Agent(tools=[calculator])                                                                                      
agent.run("what is 7^12")                                                                                              
```                                                                                                                    
                                                                                                                    
## Building a Simple Pipeline                                                                                          
                                                                                                                    
While Agents are great for getting started, they are limited to a single task. If you want to run multiple tasks in sequence, you can use Pipelines. Here's an example of a simple two-task Pipeline that uses tools and memory:           
                                                                                                                    
```python                                                                                                              
from griptape.memory.structure import ConversationMemory                                                               
from griptape.structures import Pipeline                                                                               
from griptape.tasks import ToolkitTask, PromptTask                                                                     
from griptape.tools import WebScraper, FileManager, TaskMemoryClient                                                   
                                                                                                                    
pipeline = Pipeline(conversation_memory=ConversationMemory())                                                          
pipeline.add_tasks(                                                                                                    
    ToolkitTask("{{ args[0] }}", tools=[WebScraper(), FileManager(), TaskMemoryClient(off_prompt=False)]),             
    PromptTask("Say the following in Spanish: {{ parent_output }}")                                                    
)                                                                                                                      
pipeline.run("Load https://www.griptape.ai, summarize it, and store it in griptape.txt")                               
```                                                                                                                    
                                                                                                                    
This pipeline loads a webpage, summarizes it, stores the summary in a text file, and then translates the summary into Spanish.                                                                                                               
                                                                                                                    
Note: Some models, like gpt-3.5, can perform basic arithmetic and return the correct numeric answer, although the format might be a bit unusual.