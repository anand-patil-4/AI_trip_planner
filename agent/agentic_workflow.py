from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self):
        self.tools = [
            WeatherInfoTool(),
            PlaceSearchTool(),
            CalculatorTool(),
            CurrencyConverterTool()
        ]
        self.system_prompt = SYSTEM_PROMPT



    def agent_function(self, state:MessagesState):
        ''' Main agent function'''
        user_question = state["messages"]
        '''
        Retrieves the list of chat messages from the shared state.
        messages probably contains a conversation history or the latest user prompt.
        '''
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages" : [response]}
    #This new state will replace the old one and be passed to the next node in the graph.


    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        #Creates a new StateGraph object.
        # MessagesState is the shared state structure (a Pydantic model or dict-like object).
        # This state is passed between nodes and updated as the graph progresses.

        graph_builder.add_node("agent", self.agent_function)
        """
        Adds a node named "agent" to the graph.
        This node will run the method self.agent_function (likely handles LLM/chat logic).
        This is the core decision-making node in the workflow.
        """

        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        """
        Adds another node named "tools".
        This node uses a ToolNode object, initialized with self.tools.
        This is the tool executor node, which likely calls external tools/functions based on agent decisions.
        """

        graph_builder.add_edge(START, "agent")
        """
        Adds a directed edge from START to the "agent" node.
        This tells the graph to start execution from the agent node.
        """

        graph_builder.add_conditional_edges("agent", tools_condition)
        """
        Adds conditional edges from the "agent" node based on a tools_condition function.
        This function decides which node to go to next, depending on the state.
        Typically used to decide:
        ➤ Should we call a tool ("tools")
        ➤ Or should we end (END)?
        """

        graph_builder.add_edge("tools", "agent")
        """
        Adds an edge from the "tools" node back to the "agent" node.
        Once the tool has executed, control returns to the agent for further processing or final answer.
        """

        graph_builder.add_edge("agent", END)
        """
        Adds an edge from the "agent" node to END.
        This is followed only when the agent decides the task is complete (as per tools_condition).
        """

        self.graph = graph_builder.compile()
        return self.graph




    def __call__(self):
        return self.build_graph()